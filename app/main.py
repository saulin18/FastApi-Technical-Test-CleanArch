"""
Main FastAPI application.
"""
from fastapi import FastAPI
from app.core.config import settings
from app.presentation.routers import auth_router, task_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
)

# Include routers here
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(task_router.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "FastAPI Clean Architecture TodoList API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

