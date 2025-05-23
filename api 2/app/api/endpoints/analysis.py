from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from ...core.security import verify_api_key
from ...db.database import get_db

router = APIRouter()

@router.get("/analizar")
async def analyze_stock(
    symbol: str,
    api_key_data: Dict[str, Any] = Depends(verify_api_key)
):
    """
    Analyze a stock symbol and return the latest analysis data.
    """
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")
    
    symbol = symbol.upper()
    
    async with get_db() as db:
        # Get the latest analysis for the symbol
        cursor = await db.execute("""
            SELECT * FROM stock_analysis 
            WHERE symbol = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (symbol,))
        
        analysis = await cursor.fetchone()
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail=f"No analysis found for symbol {symbol}"
            )
        
        # Format the response
        return {
            "symbol": analysis["symbol"],
            "short_term": {
                "analysis": analysis["short_term_analysis"],
                "timestamp": analysis["timestamp"]
            },
            "medium_term": {
                "analysis": analysis["medium_term_analysis"],
                "timestamp": analysis["timestamp"]
            },
            "long_term": {
                "analysis": analysis["long_term_analysis"],
                "timestamp": analysis["timestamp"]
            }
        } 