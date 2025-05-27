import uvicorn
from app.db.database import init_db
import asyncio

async def startup():
    await init_db()

if __name__ == "__main__":
    # Run database initialization
    asyncio.run(startup())
    
    # Start the FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,  # Different port from API 1
        reload=True
    ) 