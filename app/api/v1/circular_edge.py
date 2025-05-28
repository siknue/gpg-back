from fastapi import APIRouter
from app.schemas.glass import CalculationResult, CircularUniformInputScheme
from app.services.glass_calculator.glass_calculator import CalculateStress

router = APIRouter()

@router.post("/circular-uniform", response_model=CalculationResult)
async def perform_calculation_circular_uniform(input_data: CircularUniformInputScheme):
    result = CalculateStress.calculate_circular_uniform(input_data)
    return result
