from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from datetime import datetime, timedelta
from ...core.security import verify_api_key, verify_admin_route
from ...db.database import get_db
from ...models.usage import UsageLog

router = APIRouter()

@router.get("/usage/client")
async def get_client_usage(api_key: str = Depends(verify_api_key)):
    """Obtener estadísticas de uso del cliente"""
    async with get_db() as db:
        # Obtener información de la API key
        cursor = await db.execute("""
            SELECT 
                ak.*,
                p.name as plan_name,
                p.duration_days,
                p.requests_per_month,
                p.requests_per_second
            FROM api_keys ak
            LEFT JOIN plans p ON ak.plan_id = p.id
            WHERE ak.key = ?
        """, (api_key,))
        key_info = await cursor.fetchone()
        
        if not key_info:
            raise HTTPException(status_code=404, detail="API key not found")
        
        # Obtener historial de uso
        usage_history = await UsageLog.get_client_usage(db, api_key)
        
        # Obtener símbolos más consultados
        cursor = await db.execute("""
            SELECT 
                endpoint,
                COUNT(*) as count
            FROM usage_logs
            WHERE api_key = ? 
            AND endpoint LIKE '/api/v1/analizar?symbol=%'
            GROUP BY endpoint
            ORDER BY count DESC
            LIMIT 10
        """, (api_key,))
        top_symbols = await cursor.fetchall()
        
        # Calcular días restantes
        days_remaining = None
        if key_info["expires_at"]:
            days_remaining = (key_info["expires_at"] - datetime.utcnow()).days
        
        return {
            "plan_info": {
                "name": key_info["plan_name"],
                "requests_per_month": key_info["requests_per_month"],
                "requests_per_second": key_info["requests_per_second"],
                "days_remaining": days_remaining
            },
            "usage_stats": {
                "requests_this_month": key_info["requests_this_month"],
                "requests_remaining": key_info["requests_per_month"] - key_info["requests_this_month"],
                "last_used": key_info["last_used_at"]
            },
            "top_symbols": [dict(symbol) for symbol in top_symbols],
            "recent_activity": [dict(log) for log in usage_history]
        }

@router.get("/usage/admin")
async def get_admin_usage(api_key: str = Depends(verify_admin_route)):
    """Obtener estadísticas globales de uso (solo admin)"""
    async with get_db() as db:
        # Estadísticas generales
        general_stats = await UsageLog.get_global_usage(db)
        
        # Uso por plan
        cursor = await db.execute("""
            SELECT 
                p.name as plan_name,
                COUNT(DISTINCT ak.key) as client_count,
                SUM(ul.count) as total_requests
            FROM plans p
            LEFT JOIN api_keys ak ON p.id = ak.plan_id
            LEFT JOIN (
                SELECT api_key, COUNT(*) as count
                FROM usage_logs
                WHERE timestamp >= datetime('now', '-30 days')
                GROUP BY api_key
            ) ul ON ak.key = ul.api_key
            GROUP BY p.id
        """)
        plan_stats = await cursor.fetchall()
        
        # Símbolos más consultados globalmente
        cursor = await db.execute("""
            SELECT 
                endpoint,
                COUNT(*) as count
            FROM usage_logs
            WHERE endpoint LIKE '/api/v1/analizar?symbol=%'
            AND timestamp >= datetime('now', '-30 days')
            GROUP BY endpoint
            ORDER BY count DESC
            LIMIT 20
        """)
        top_symbols = await cursor.fetchall()
        
        return {
            "general_stats": dict(general_stats),
            "plan_stats": [dict(stat) for stat in plan_stats],
            "top_symbols": [dict(symbol) for symbol in top_symbols]
        }

@router.get("/usage/endpoints")
async def get_endpoint_stats(api_key: str = Depends(verify_admin_route)):
    """Obtener estadísticas por endpoint (solo admin)"""
    async with get_db() as db:
        endpoint_stats = await UsageLog.get_endpoint_stats(db)
        return [dict(stat) for stat in endpoint_stats]

@router.get("/usage/clients")
async def get_client_stats(api_key: str = Depends(verify_admin_route)):
    """Obtener estadísticas por cliente (solo admin)"""
    async with get_db() as db:
        client_stats = await UsageLog.get_client_stats(db)
        return [dict(stat) for stat in client_stats]

@router.post("/usage/cleanup")
async def cleanup_old_logs(api_key: str = Depends(verify_admin_route)):
    """Limpiar registros de uso antiguos (solo admin)"""
    async with get_db() as db:
        await UsageLog.cleanup_old_logs(db)
        return {"message": "Old usage logs cleaned up successfully"}