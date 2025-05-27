from fastapi import APIRouter
from app.services.glass_calculator.twoside.uniform import TwoSideUniformLoadGlass
from app.services.glass_calculator.calculator import CalculateStress
from app.schemas.glass import (
    TwoSideUniformInputScheme,
    CalculationResult,
)

router = APIRouter()

@router.post("/two-uniform", response_model=CalculationResult)
async def perform_calculation_two_uniform(input_data: TwoSideUniformInputScheme):
    result = CalculateStress.calculate_twoside_uniform(input_data)
    return result