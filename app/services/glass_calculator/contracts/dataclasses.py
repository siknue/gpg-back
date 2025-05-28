from dataclasses import dataclass

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