from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from ...core.security import verify_api_key
from ...db.database import get_db
import sqlite3
from datetime import datetime

router = APIRouter()

@router.get("/analyze/{symbol}")
async def analyze_symbol(
    symbol: str,
    api_key: dict = Depends(verify_api_key)
):
    """
    Obtiene el último análisis para un símbolo específico y registra el uso de la API
    """
    try:
        # Conectar a la base de datos de análisis de stocks
        async with get_db() as db:
            # Buscar el último análisis para el símbolo
            cursor = await db.execute("""
                SELECT 
                    symbol,
                    timestamp,
                    short_term,
                    medium_term,
                    long_term
                FROM analysis
                WHERE symbol = ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (symbol.upper(),))
            
            analysis = await cursor.fetchone()
            
            if not analysis:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontró análisis para el símbolo {symbol}"
                )
            
            # Obtener información de uso de la API key
            cursor = await db.execute("""
                SELECT 
                    requests_this_month,
                    requests_per_month,
                    expires_at
                FROM api_keys
                WHERE key = ?
            """, (api_key["key"],))
            
            key_info = await cursor.fetchone()
            
            # Registrar el uso de la API
            await db.execute("""
                INSERT INTO api_usage (
                    api_key,
                    endpoint,
                    symbol,
                    timestamp
                ) VALUES (?, ?, ?, ?)
            """, (
                api_key["key"],
                f"/analyze/{symbol}",
                symbol.upper(),
                datetime.utcnow()
            ))
            
            await db.commit()
            
            # Formatear respuesta
            return {
                "symbol": analysis["symbol"],
                "timestamp": analysis["timestamp"],
                "analysis": {
                    "short_term": analysis["short_term"],
                    "medium_term": analysis["medium_term"],
                    "long_term": analysis["long_term"]
                },
                "api_key_info": {
                    "requests_used": key_info["requests_this_month"],
                    "requests_remaining": key_info["requests_per_month"] - key_info["requests_this_month"],
                    "expires_at": key_info["expires_at"]
                }
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )