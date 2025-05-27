from typing import List
from pydantic import BaseModel, PositiveFloat

class CalculationResult(BaseModel):
    sigma: float # 最大応力
    delta: float # 最大変位 

class FourSideUniformInputScheme(BaseModel):
    a: PositiveFloat# 短辺寸法（mm）
    b: PositiveFloat# 長辺寸法（mm）
    t: List[PositiveFloat]# 板厚（mm）
    w: PositiveFloat# 風圧（Pa）
    nu: float = 0.22 # ポアソン比（ガラスの標準値）
    E: float = 71600 # ヤング係数（ガラスの標準値）

class FourSidePartialInputScheme(BaseModel):
    a: PositiveFloat# 短辺寸法（mm）
    b: PositiveFloat# 長辺寸法（mm）
    a1: PositiveFloat# 短辺荷重寸法（mm）
    b1: PositiveFloat# 長辺荷重寸法（mm）
    t: List[PositiveFloat]# 板厚（mm）
    w: PositiveFloat# 風圧（Pa）
    nu: float = 0.22 # ポアソン比（ガラスの標準値）
    E: float = 71600 # ヤング係数（ガラスの標準値）
    
class ThreeSideUniformInputScheme(BaseModel):
    free: PositiveFloat# 自由辺寸法（mm）
    fix: PositiveFloat# 固定辺寸法（mm）
    t: List[PositiveFloat]# 板厚（mm）
    w: PositiveFloat# 風圧（Pa）
    nu: float = 0.22 # ポアソン比（ガラスの標準値）
    E: float = 71600 # ヤング係数（ガラスの標準値）

class TwoSideUniformInputScheme(BaseModel):
    free: PositiveFloat# 自由辺寸法（mm）
    fix: PositiveFloat# 固定辺寸法（mm）
    t: List[PositiveFloat]# 板厚（mm）
    w: PositiveFloat# 風圧（Pa）
    nu: float = 0.22 # ポアソン比（ガラスの標準値）
    E: float = 71600 # ヤング係数（ガラスの標準値）

class CircularUniformInputScheme(BaseModel):
    D: PositiveFloat# 直径寸法（mm）
    t: List[PositiveFloat]# 板厚（mm）
    w: PositiveFloat# 風圧（Pa）
    nu: float = 0.22 # ポアソン比（ガラスの標準値）
    E: float = 71600 # ヤング係数（ガラスの標準値）
