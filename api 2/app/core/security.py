from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import APIKeyHeader
from datetime import datetime, timedelta
from ..db.database import get_db
from ..core.config import settings
from typing import Optional

api_key_header = APIKeyHeader(name="X-API-KEY")

async def verify_api_key(api_key: str = Security(api_key_header)) -> dict:
    """Verify API key and return key data if valid."""
    async with get_db() as db:
        # Check if API key exists and is active
        cursor = await db.execute(
            "SELECT * FROM api_keys WHERE key = ? AND is_active = TRUE",
            (api_key,)
        )
        key_data = await cursor.fetchone()
        
        if not key_data:
            raise HTTPException(
                status_code=401,
                detail="Invalid or inactive API key"
            )
        
        # Check if key has expired
        if key_data["expires_at"] and key_data["expires_at"] < datetime.utcnow():
            raise HTTPException(
                status_code=401,
                detail="API key has expired"
            )
        
        # Check monthly limit
        if key_data["requests_this_month"] >= key_data["requests_per_month"]:
            raise HTTPException(
                status_code=429,
                detail="Monthly request limit exceeded"
            )
        
        # Update last used timestamp
        await db.execute(
            "UPDATE api_keys SET last_used_at = ? WHERE key = ?",
            (datetime.utcnow(), api_key)
        )
        
        # Increment monthly requests
        await db.execute(
            "UPDATE api_keys SET requests_this_month = requests_this_month + 1 WHERE key = ?",
            (api_key,)
        )
        
        await db.commit()
        
        return dict(key_data)

async def verify_admin_access(api_key: str = Security(api_key_header)) -> dict:
    """Verify that the API key has admin privileges."""
    key_data = await verify_api_key(api_key)
    
    if not key_data.get("is_admin", False):
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    
    return key_data

async def verify_admin_route(request: Request, api_key: str = Security(api_key_header)) -> dict:
    """Verify admin access and additional security for admin routes."""
    # Verify admin privileges
    key_data = await verify_admin_access(api_key)
    
    # Additional security checks for admin routes
    if not request.url.path.startswith("/api/v1/admin/"):
        raise HTTPException(
            status_code=403,
            detail="Invalid admin route access"
        )
    
    # Check for specific admin route patterns
    admin_patterns = [
        "/api/v1/admin/users",
        "/api/v1/admin/keys",
        "/api/v1/admin/stats"
    ]
    
    if not any(request.url.path.startswith(pattern) for pattern in admin_patterns):
        raise HTTPException(
            status_code=403,
            detail="Invalid admin endpoint"
        )
    
    return key_data

async def verify_admin(username: str, password: str):
    if username != settings.ADMIN_USERNAME or password != settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials"
        )
    return True 