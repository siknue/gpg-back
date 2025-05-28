from fastapi import APIRouter
from app.services.glass_calculator.glass_calculator import CalculateStress
from app.schemas.glass import (
    FourSidePartialInputScheme,
    FourSideUniformInputScheme,
    CalculationResult,
)

router = APIRouter()

@router.post("/four-partial", response_model=CalculationResult)
async def perform_calculation_four_partial(input_data: FourSidePartialInputScheme):
    result = CalculateStress.calculate_fourside_partial(input_data)
    return result

@router.post("/four-uniform", response_model=CalculationResult)
async def perform_calculation_four_uniform(input_data: FourSideUniformInputScheme):
    print(input_data)
    result = CalculateStress.calculate_fourside_uniform(input_data)
    return result