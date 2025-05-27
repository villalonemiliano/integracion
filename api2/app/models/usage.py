from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UsageLog(BaseModel):
    """Modelo para registrar el uso de la API"""
    api_key: str
    endpoint: str
    method: str
    ip: str
    duration: float
    timestamp: datetime
    status_code: Optional[int] = None
    error_message: Optional[str] = None

    async def save(self, db):
        """Guarda el registro de uso en la base de datos"""
        query = """
            INSERT INTO usage_logs (
                api_key, endpoint, method, ip, duration, 
                timestamp, status_code, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        await db.execute(
            query,
            (
                self.api_key,
                self.endpoint,
                self.method,
                self.ip,
                self.duration,
                self.timestamp,
                self.status_code,
                self.error_message
            )
        )
        await db.commit()

    @classmethod
    async def get_client_usage(cls, db, api_key: str, days: int = 30):
        """Obtiene el uso de un cliente específico"""
        query = """
            SELECT 
                endpoint,
                method,
                timestamp,
                duration,
                status_code,
                error_message
            FROM usage_logs
            WHERE api_key = ?
            AND timestamp >= datetime('now', ? || ' days')
            ORDER BY timestamp DESC
        """
        cursor = await db.execute(query, (api_key, -days))
        return await cursor.fetchall()

    @classmethod
    async def get_global_usage(cls, db, days: int = 30):
        """Obtiene estadísticas globales de uso"""
        query = """
            SELECT 
                COUNT(*) as total_requests,
                COUNT(DISTINCT api_key) as unique_clients,
                AVG(duration) as avg_duration,
                COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count
            FROM usage_logs
            WHERE timestamp >= datetime('now', ? || ' days')
        """
        cursor = await db.execute(query, (-days,))
        return await cursor.fetchone()

    @classmethod
    async def get_endpoint_stats(cls, db, days: int = 30):
        """Obtiene estadísticas por endpoint"""
        query = """
            SELECT 
                endpoint,
                COUNT(*) as request_count,
                AVG(duration) as avg_duration,
                COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count
            FROM usage_logs
            WHERE timestamp >= datetime('now', ? || ' days')
            GROUP BY endpoint
            ORDER BY request_count DESC
        """
        cursor = await db.execute(query, (-days,))
        return await cursor.fetchall()

    @classmethod
    async def get_client_stats(cls, db, days: int = 30):
        """Obtiene estadísticas por cliente"""
        query = """
            SELECT 
                api_key,
                COUNT(*) as request_count,
                AVG(duration) as avg_duration,
                COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count
            FROM usage_logs
            WHERE timestamp >= datetime('now', ? || ' days')
            GROUP BY api_key
            ORDER BY request_count DESC
        """
        cursor = await db.execute(query, (-days,))
        return await cursor.fetchall()

    @classmethod
    async def cleanup_old_logs(cls, db, days: int = 90):
        """Elimina registros de uso antiguos"""
        query = """
            DELETE FROM usage_logs
            WHERE timestamp < datetime('now', ? || ' days')
        """
        await db.execute(query, (-days,))
        await db.commit() 