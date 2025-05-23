import aiosqlite
from contextlib import asynccontextmanager
from ..core.config import settings

@asynccontextmanager
async def get_db():
    async with aiosqlite.connect(settings.DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        yield db

async def init_db():
    async with get_db() as db:
        # Create API keys table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key TEXT PRIMARY KEY,
                user_id INTEGER,
                plan_id INTEGER,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP,
                requests_this_month INTEGER DEFAULT 0,
                requests_per_second INTEGER,
                requests_per_month INTEGER
            )
        """)
        
        # Create usage logs table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key TEXT,
                endpoint TEXT,
                method TEXT,
                ip TEXT,
                duration REAL,
                timestamp TIMESTAMP,
                FOREIGN KEY (api_key) REFERENCES api_keys(key)
            )
        """)
        
        # Create plans table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                requests_per_second INTEGER,
                requests_per_month INTEGER,
                price REAL,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        await db.commit() 