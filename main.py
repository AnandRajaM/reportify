"""
FastAPI Main Application Entry Point
Run with: uvicorn main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.router import router as api_v1_router

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Medical Report Generator - Converting JSON to Professional PDFs",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routers
app.include_router(
    api_v1_router,
    prefix=settings.API_V1_PREFIX,
    tags=["api-v1"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Reportify API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "health": "/api/v1/reports/health"
    }


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📚 API Documentation: http://localhost:8000/api/docs")
    print(f"🔧 API Version: {settings.API_V1_PREFIX}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    from app.core.database import db
    db.disconnect()
    print("👋 Application shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )




