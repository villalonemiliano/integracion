from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional
from ...core.security import verify_api_key
from ...core.api_key_manager import APIKeyManager
from ...db.database import get_db

router = APIRouter()

@router.get("/search")
async def search(
    query: str,
    request: Request,
    api_key: str = Depends(verify_api_key)
):
    """Search endpoint that includes API key information."""
    # Get API key information
    key_info = await APIKeyManager.get_api_key_info(api_key)
    
    # Your existing search logic here
    # ...
    
    return {
        "results": [],  # Your search results here
        "api_key_info": {
            "name": key_info["name"],
            "email": key_info["email"],
            "requests_remaining": key_info["requests_per_month"] - key_info["requests_this_month"],
            "expires_at": key_info["expires_at"]
        }
    } 