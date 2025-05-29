from fastapi import APIRouter
from app.api.v1 import four_edge, three_edge, two_edge, circular_edge, health_check, auth

router = APIRouter()

prefix_health = "/v1/health"
router.include_router(auth.router, prefix=prefix_health, tags=["Authentication"])
router.include_router(health_check.router, prefix=prefix_health, tags=["Health Check"])

prefix_glass = "/v1/glass"
router.include_router(four_edge.router, prefix=prefix_glass, tags=["四辺支持"])
router.include_router(three_edge.router, prefix=prefix_glass, tags=["三辺支持"])
router.include_router(two_edge.router, prefix=prefix_glass, tags=["二辺支持"])
router.include_router(circular_edge.router, prefix=prefix_glass, tags=["円周支持"])