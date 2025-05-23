import secrets
import string
from datetime import datetime, timedelta
from typing import Optional
from ..db.database import get_db

class APIKeyManager:
    @staticmethod
    def generate_api_key(prefix: str = "sk") -> str:
        """Generate a secure API key with a prefix."""
        # Generate 32 random characters
        random_chars = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        return f"{prefix}_{random_chars}"

    @staticmethod
    async def create_api_key(
        name: str,
        email: str,
        is_admin: bool = False,
        requests_per_month: int = 10000,
        expires_at: Optional[datetime] = None
    ) -> dict:
        """Create a new API key with specified permissions."""
        api_key = APIKeyManager.generate_api_key(prefix="sk_admin" if is_admin else "sk")
        
        async with get_db() as db:
            # Check if email already has an API key
            cursor = await db.execute(
                "SELECT * FROM api_keys WHERE email = ?",
                (email,)
            )
            existing_key = await cursor.fetchone()
            if existing_key:
                raise ValueError(f"Email {email} already has an API key")

            await db.execute("""
                INSERT INTO api_keys (
                    key, name, email, is_admin, is_active, 
                    requests_per_month, requests_this_month,
                    created_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                api_key,
                name,
                email,
                is_admin,
                True,
                requests_per_month,
                0,
                datetime.utcnow(),
                expires_at
            ))
            await db.commit()
        
        return {
            "api_key": api_key,
            "name": name,
            "email": email,
            "is_admin": is_admin,
            "expires_at": expires_at
        }

    @staticmethod
    async def get_api_key_by_email(email: str) -> Optional[dict]:
        """Get API key information by email."""
        async with get_db() as db:
            cursor = await db.execute(
                "SELECT * FROM api_keys WHERE email = ? AND is_active = TRUE",
                (email,)
            )
            key_data = await cursor.fetchone()
            return dict(key_data) if key_data else None

    @staticmethod
    async def revoke_api_key(api_key: str) -> bool:
        """Revoke an API key by setting it as inactive."""
        async with get_db() as db:
            await db.execute(
                "UPDATE api_keys SET is_active = FALSE WHERE key = ?",
                (api_key,)
            )
            await db.commit()
        return True

    @staticmethod
    async def get_api_key_info(api_key: str) -> Optional[dict]:
        """Get information about an API key."""
        async with get_db() as db:
            cursor = await db.execute(
                "SELECT * FROM api_keys WHERE key = ?",
                (api_key,)
            )
            key_data = await cursor.fetchone()
            return dict(key_data) if key_data else None 