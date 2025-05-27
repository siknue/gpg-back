from fastapi import APIRouter
from app.api.v1 import four_edge, three_edge, two_edge, circular_edge, health_check, auth

router = APIRouter()
router.include_router(auth.router, prefix="/v1", tags=["Authentication"])
router.include_router(health_check.router, prefix="/v1", tags=["Health Check"])
router.include_router(four_edge.router, prefix="/v1", tags=["四辺支持"])
router.include_router(three_edge.router, prefix="/v1", tags=["三辺支持"])
router.include_router(two_edge.router, prefix="/v1", tags=["二辺支持"])
router.include_router(circular_edge.router, prefix="/v1", tags=["円周支持"])