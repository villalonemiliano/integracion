from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from datetime import datetime
import time
from typing import Optional
import sqlite3
import os

from .core.config import settings
from .api.endpoints import analysis, admin
from .core.security import verify_api_key
from .db.database import get_db
from .models.usage import UsageLog

app = FastAPI(
    title="Stock Analysis API",
    description="API for accessing stock analysis data",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key header
api_key_header = APIKeyHeader(name="X-API-KEY")

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Log the request if it's an API endpoint
    if request.url.path.startswith("/api/"):
        api_key = request.headers.get("X-API-KEY")
        if api_key:
            async with get_db() as db:
                log = UsageLog(
                    api_key=api_key,
                    endpoint=request.url.path,
                    method=request.method,
                    ip=request.client.host,
                    duration=duration,
                    timestamp=datetime.utcnow()
                )
                await log.save(db)
    
    return response

# Include routers
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Stock Analysis API is running"} 