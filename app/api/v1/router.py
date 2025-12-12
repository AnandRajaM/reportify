"""
API v1 Router
Aggregates all v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import reports

router = APIRouter()

# Include all endpoint routers
router.include_router(
    reports.router,
    prefix="/reports",
    tags=["reports"]
)
