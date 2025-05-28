from typing import Dict
from app.services.glass_calculator.glass_material import GlassMaterial
from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.contracts.interfaces import IPlate
from app.services.binary_search import binary_search
from app.services.binary_search.binary_search import BisectTypeEnum

class TwoSideUniformLoadGlass(IPlate):
    """
    TwoEdgeSupportedUniformLoadGlass クラス
    二辺支持均等荷重を受けるガラスの応力と変位を計算するクラスです。
    計算には、係数テーブルを使用しており、適用範囲に制限があります。
    範囲外の入力値に対しては、例外をraiseします。
    """
    
    def __init__(self, free_edge: float, fixed_edge: float, thickness: GlassLayer, w: float, material:GlassMaterial):
        """
        コンストラクタ
        
        Args:
            free_edge: フリー辺の長さ [mm]
            fixed_edge: 固定辺の長さ [mm] 
            thickness: ガラスレイヤークラス
            w: 荷重 [N/mm2]
            material: マテリアル
            
        Raises:
            ValueError: 固定辺/フリー < 0.5の場合
        """
        self.edge_length_ratio = fixed_edge / free_edge
        self._validate_edge_length(free_edge, fixed_edge)
        self.a = free_edge
        self.b = fixed_edge
        self.layer = thickness
        self.w = w
        self.material = material
        
        coeff = self._calculate_coeff()
        self.alpha = coeff["alpha"]
        self.beta = coeff["beta"]
    
    def _validate_edge_length(self, a: float, b: float) -> None:
        """
        エッジの長さのバリデーション
        
        Args:
            a: フリー辺の長さ [mm]
            b: 固定辺の長さ [mm]
            
        Raises:
            ValueError: 辺長比が計算係数テーブルの適用範囲外の場合
        """
        edge_length_ratio = b / a
        if edge_length_ratio < 0.5:
            raise ValueError("b/a is smaller than 0.5. use FEM instead")
    
    def _calculate_coeff(self) -> Dict[str, float]:
        """
        係数計算
        
        Returns:
            Dict[str, float]: 応力、変位計算用係数（alpha, beta）
            
        Raises:
            ValueError: 係数テーブルの適用範囲外の場合
        """
        coeff = {
            "bByA": [0.5, 1, 2, float('inf')],
            "beta": [0.765, 0.782, 0.791, 0.791],
            "alpha": [0.160, 0.163, 0.165, 0.165],
        }
        
        index = binary_search.binary_search(coeff["bByA"], self.edge_length_ratio, BisectTypeEnum.LEFT)
        alpha = coeff["alpha"][index]
        beta = coeff["beta"][index]
        return {"alpha": alpha, "beta": beta}
    
    def calculate_stress(self) -> float:
        """
        応力計算
        
        Returns:
            float: 板の応力 [N/mm2]
        """
        thickness = self.layer.get_equivalent_thickness()
        sigma = (self.beta * (self.w * self.a ** 2)) / thickness ** 2
        return sigma
    
    def calculate_displacement(self) -> float:
        """
        変位計算
        
        Returns:
            float: 板の変位 [mm]
        """
        e = self.material.E
        thickness = self.layer.get_equivalent_thickness()
        delta = (self.alpha * (self.w * self.a ** 4)) / (thickness ** 3 * e)
        return delta
