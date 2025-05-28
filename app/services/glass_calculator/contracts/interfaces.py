from typing import Protocol

from app.services.glass_calculator.glass_material import GlassMaterial
from app.services.glass_calculator.glass_layer import GlassLayer

class IPlate(Protocol):
    b: float
    a: float
    edge_length_ratio: float
    layer: GlassLayer
    material: GlassMaterial
    
    def calculate_stress(self) -> float:
        ...
    
    def calculate_displacement(self) -> float:
        ...