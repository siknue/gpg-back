from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from app.services.glass_calculator.material import Material
from app.services.glass_calculator.glass_layer import GlassLayer

class GlassTypeEnum(Enum):
    FLOAT = "float"
    WIRED = "wired"
    WIRE_PATTERNED = "wirePatterend"
    TEMPERED = "tempered"
    DOUBLE = "double"

class InterlayerMaterialTypeEnum(Enum):
    SG = "sg"
    PVB = "pvb"
    EVA = "eva"


@dataclass
class FractureStrength:
    """
    破壊応力
    """
    inplane: float
    edge: float

@dataclass
class StressLimits:
    """
    面内、エッジ許容応力
    """
    inplane: float
    edge: float

@dataclass
class AllowableStressTerms:
    """
    長期、短期許容応力
    """
    shortTerm: StressLimits
    longTerm: StressLimits

@dataclass
class IAllowableStress:
    fracturesStrength: FractureStrength
    allowableStress: AllowableStressTerms

class IPlate(Protocol):
    b: float
    a: float
    edge_length_ratio: float
    layer: GlassLayer
    material: Material
    
    def calculate_stress(self) -> float:
        ...
    
    def calculate_displacement(self) -> float:
        ...