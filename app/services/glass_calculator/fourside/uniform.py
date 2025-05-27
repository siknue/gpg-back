from app.services.glass_calculator.material import Material
from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.contracts import  IPlate
from app.services.binary_search import binary_search
from app.services.binary_search.binary_search import BisectTypeEnum

class FourSideUniformLoadGlass(IPlate):
    """四辺支持ガラスの応力・変位計算クラス"""
    
    def __init__(self, short_edge: float, long_edge: float, layer: GlassLayer, w: float, material:Material):
        """
        四辺支持された均一荷重下のガラス板の初期化
        
        Args:
            short_edge: 短辺長さ (a) [mm]
            long_edge: 長辺長さ (b) [mm]
            layer: ガラス層オブジェクト
            w: 均一荷重 [N/mm²]
            material: 材質クラス 
            
        Raises:
            ValueError: 短辺が長辺より長い場合、または辺長比が5を超える場合
        """
        self.edge_length_ratio = long_edge / short_edge
        max_ratio = 5
        min_ratio = 1

        if short_edge > long_edge:
            raise ValueError("短辺が長辺より長くなることはできません")
            
        # b>aより辺長比が1を下回ることはないため、上限のみチェックする
        if self.edge_length_ratio > max_ratio:
            raise ValueError("b/aが5を超えています。代わりにFEMを使用してください")

        self.a = short_edge
        self.b = long_edge
        self.layer = layer
        self.w = w
        self.material = material

    def _calculate_coeff(self):
        """応力・変位計算用の補間係数を計算"""
        coeff = {
            "b_by_a": [1, 1.2, 1.5, 2, 3, 4, 5],
            "beta": [0.272, 0.362, 0.476, 0.603, 0.711, 0.74, 0.748],
            "alpha": [0.047, 0.065, 0.088, 0.116, 0.139, 0.146, 0.148],
        }

        index = binary_search.binary_search(coeff["b_by_a"], self.edge_length_ratio, BisectTypeEnum.LEFT)
        alpha = coeff["alpha"][index]
        beta = coeff["beta"][index]
        return {"alpha": alpha, "beta": beta}

    def calculate_stress(self) -> float:
        """
        ガラス板の応力を計算
        
        Returns:
            float: 板の応力 [N/mm²]
        """
        coeff = self._calculate_coeff()
        beta = coeff["beta"]
        layer = self.layer.get_equivalent_thickness()
        print("layer",layer)
        sigma = (beta * (self.w * self.a ** 2)) / layer ** 2
        
        return sigma

    def calculate_displacement(self) -> float:
        """
        ガラス板の変位を計算
        
        Returns:
            float: 板の変位 [mm]
        """
        coeff = self._calculate_coeff()
        alpha = coeff["alpha"]
        E = self.material.E
        layer = self.layer.get_equivalent_thickness()
        delta = (alpha * (self.w * self.a ** 4)) / (layer ** 3 * E)
        print(delta)
        return delta
