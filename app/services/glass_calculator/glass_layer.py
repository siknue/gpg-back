from enum import Enum
from typing import Sequence
from app.services.glass_calculator.contracts.enums import InterlayerMaterialTypeEnum
class GlassLayer:
    def __init__(self, layers: Sequence[float], interlayer_material: InterlayerMaterialTypeEnum):
        self.layers = layers
        self.interlayer_material = interlayer_material
    
    def get_outer_layer_thickness(self) -> Sequence[float]:
        """外側レイヤーの厚さを返す"""
        outer_layer1 = self.layers[0]
        outer_layer2 = self.layers[-1]
        return [outer_layer1, outer_layer2]
    
    def get_equivalent_thickness(self) -> float:
        """等価厚さを計算して返す"""
        total_thickness = sum(self.layers)
        
        # Todo: SG以外の実装を行う。
        if self.interlayer_material == InterlayerMaterialTypeEnum.SG:
            return total_thickness
        
        # SG以外は等価板厚を計算
        else:
            equivalent_thickness = 0.866 * total_thickness - 0.268
            return equivalent_thickness