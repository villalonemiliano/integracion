from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import secrets
from ...core.security import verify_admin, verify_admin_route
from ...db.database import get_db
from ...core.api_key_manager import APIKeyManager

router = APIRouter()

@router.post("/plans")
async def create_plan(
    name: str = Body(...),
    requests_per_second: int = Body(...),
    requests_per_month: int = Body(...),
    price: float = Body(...),
    admin_auth: bool = Depends(verify_admin)
):
    """Create a new plan"""
    async with get_db() as db:
        await db.execute("""
            INSERT INTO plans (name, requests_per_second, requests_per_month, price)
            VALUES (?, ?, ?, ?)
        """, (name, requests_per_second, requests_per_month, price))
        await db.commit()
        return {"message": "Plan created successfully"}

@router.get("/plans")
async def list_plans(admin_auth: bool = Depends(verify_admin)):
    """List all plans"""
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM plans WHERE is_active = TRUE")
        plans = await cursor.fetchall()
        return [dict(plan) for plan in plans]

@router.post("/api-keys")
async def create_api_key(
    user_id: int = Body(...),
    plan_id: int = Body(...),
    admin_auth: bool = Depends(verify_admin)
):
    """Create a new API key for a user"""
    # Generate a secure API key
    api_key = secrets.token_urlsafe(32)
    
    async with get_db() as db:
        # Get plan details
        cursor = await db.execute("SELECT * FROM plans WHERE id = ?", (plan_id,))
        plan = await cursor.fetchone()
        
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        # Create API key
        await db.execute("""
            INSERT INTO api_keys (
                key, user_id, plan_id, requests_per_second, requests_per_month
            ) VALUES (?, ?, ?, ?, ?)
        """, (api_key, user_id, plan_id, plan["requests_per_second"], plan["requests_per_month"]))
        
        await db.commit()
        return {"api_key": api_key}

@router.get("/usage-stats")
async def get_usage_stats(admin_auth: bool = Depends(verify_admin)):
    """Get usage statistics"""
    async with get_db() as db:
        # Get total requests by client
        cursor = await db.execute("""
            SELECT api_key, COUNT(*) as total_requests
            FROM usage_logs
            GROUP BY api_key
        """)
        client_stats = await cursor.fetchall()
        
        # Get most requested symbols
        cursor = await db.execute("""
            SELECT endpoint, COUNT(*) as count
            FROM usage_logs
            WHERE endpoint LIKE '/api/v1/analizar?symbol=%'
            GROUP BY endpoint
            ORDER BY count DESC
            LIMIT 10
        """)
        symbol_stats = await cursor.fetchall()
        
        # Get hourly statistics
        cursor = await db.execute("""
            SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
            FROM usage_logs
            GROUP BY hour
            ORDER BY hour
        """)
        hourly_stats = await cursor.fetchall()
        
        return {
            "client_stats": [dict(stat) for stat in client_stats],
            "symbol_stats": [dict(stat) for stat in symbol_stats],
            "hourly_stats": [dict(stat) for stat in hourly_stats]
        }

@router.post("/keys/generate")
async def generate_api_key(
    name: str,
    is_admin: bool = False,
    requests_per_month: int = 10000,
    expires_in_days: Optional[int] = None,
    key_data: dict = Depends(verify_admin_route)
):
    """Generate a new API key with specified permissions."""
    expires_at = None
    if expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    new_key = await APIKeyManager.create_api_key(
        name=name,
        is_admin=is_admin,
        requests_per_month=requests_per_month,
        expires_at=expires_at
    )
    
    return {
        "message": "API key generated successfully",
        "api_key": new_key["api_key"],
        "name": new_key["name"],
        "is_admin": new_key["is_admin"],
        "expires_at": new_key["expires_at"]
    }

@router.post("/keys/revoke/{api_key}")
async def revoke_api_key(
    api_key: str,
    key_data: dict = Depends(verify_admin_route)
):
    """Revoke an existing API key."""
    success = await APIKeyManager.revoke_api_key(api_key)
    if success:
        return {"message": "API key revoked successfully"}
    raise HTTPException(status_code=404, detail="API key not found")

@router.get("/keys/info/{api_key}")
async def get_api_key_info(
    api_key: str,
    key_data: dict = Depends(verify_admin_route)
):
    """Get information about an API key."""
    info = await APIKeyManager.get_api_key_info(api_key)
    if info:
        return info
    raise HTTPException(status_code=404, detail="API key not found")

@router.post("/generate-api-key")
async def generate_api_key_from_panel(
    email: str = Body(...),
    name: str = Body(...),
    requests_per_month: int = Body(10000),
    expires_in_days: Optional[int] = Body(None),
    admin_auth: bool = Depends(verify_admin)
):
    """Generate a new API key from the admin panel."""
    try:
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        new_key = await APIKeyManager.create_api_key(
            name=name,
            email=email,
            is_admin=False,
            requests_per_month=requests_per_month,
            expires_at=expires_at
        )
        
        return {
            "message": "API key generated successfully",
            "api_key": new_key["api_key"],
            "name": new_key["name"],
            "email": new_key["email"],
            "expires_at": new_key["expires_at"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating API key")

@router.get("/api-keys")
async def list_api_keys(admin_auth: bool = Depends(verify_admin)):
    """List all API keys."""
    async with get_db() as db:
        cursor = await db.execute("""
            SELECT id, name, email, is_admin, is_active, 
                   requests_per_month, requests_this_month,
                   created_at, last_used_at, expires_at
            FROM api_keys
            ORDER BY created_at DESC
        """)
        keys = await cursor.fetchall()
        return [dict(key) for key in keys] 