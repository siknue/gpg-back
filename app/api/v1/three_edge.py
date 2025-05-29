from fastapi import APIRouter
from app.services.glass_calculator.glass_calculator import CalculateStress
from app.schemas.glass import (
    ThreeSideUniformInputScheme,
    CalculationResult,
)

router = APIRouter()

@router.post("/three-uniform", response_model=CalculationResult)
async def perform_calculation_three_uniform(input_data: ThreeSideUniformInputScheme):
    result = CalculateStress.calculate_threeside_uniform(input_data)
    return result