import aiosqlite
from ..core.config import settings

async def get_db():
    """Obtener conexión a la base de datos"""
    db = await aiosqlite.connect(settings.DATABASE_URL)
    db.row_factory = aiosqlite.Row
    return db

async def init_db():
    """Inicializar la base de datos con todas las tablas necesarias"""
    async with get_db() as db:
        # Tabla de planes
        await db.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                requests_per_second INTEGER NOT NULL,
                requests_per_month INTEGER NOT NULL,
                duration_days INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de API keys
        await db.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key TEXT PRIMARY KEY,
                user_email TEXT NOT NULL,
                plan_id INTEGER,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP,
                requests_this_month INTEGER DEFAULT 0,
                requests_per_second INTEGER,
                requests_per_month INTEGER,
                expires_at TIMESTAMP,
                FOREIGN KEY (plan_id) REFERENCES plans(id)
            )
        """)
        
        # Tabla de uso de API
        await db.execute("""
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                symbol TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (api_key) REFERENCES api_keys(key)
            )
        """)
        
        # Verificar si existe la tabla de análisis
        cursor = await db.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='analysis'
        """)
        if not await cursor.fetchone():
            # Si no existe, crear la tabla de análisis
            await db.execute("""
                CREATE TABLE IF NOT EXISTS analysis (
                    symbol TEXT,
                    timestamp DATETIME,
                    short_term TEXT,
                    medium_term TEXT,
                    long_term TEXT,
                    PRIMARY KEY (symbol, timestamp)
                )
            """)
        
        await db.commit()