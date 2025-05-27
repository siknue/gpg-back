from typing import Dict, List

from app.services.glass_calculator.material import Material
from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.contracts import  IPlate
from app.services.binary_search import binary_search
from app.services.binary_search.binary_search import BisectTypeEnum

class FourSidePartialLoadGlass(IPlate):
    """
    FourEdgeSupportedPartialUniformLoadGlass クラス
    4辺支持部分均等荷重を受けるガラスの応力と変位を計算するクラスです。
    計算には、係数テーブルを使用しており、適用範囲に制限があります。
    範囲外の入力値に対しては、例外をraiseします。
    """
    
    def __init__(
        self,
        a: float,
        b: float,
        layer: GlassLayer,
        w: float,
        a1: float,
        b1: float,
        material: Material
    ):
        """
        コンストラクタ
        
        Args:
            a: 短辺の長さ [mm]
            b: 長辺の長さ [mm]
            thickness: ガラスレイヤークラス
            w: 荷重 [N/mm2]
            a1: 短辺方向の荷重負荷長 [mm]
            b1: 長辺方向の荷重負荷長 [mm]
            material: マテリアルクラス
            
        Raises:
            ValueError: 短辺が長辺より大きい場合、または辺長比が範囲外の場合
        """
        self.edge_length_ratio = b / a
        
        self._validate_edge_length(a, b)
        self.a = a
        self.b = b
        self.layer = layer
        self.w = w
        self.a1 = a1
        self.b1 = b1
        self.material = material
        
        coeff_result = self._calculate_coeff()
        self.alpha = coeff_result["alpha"]
        self.beta = coeff_result["beta"]
        
        # 係数テーブルの定義（クラス変数として定義）
    
    # 係数テーブルをクラス変数として定義
    coeff = [
        # bByA: 1
        [
            # a'/a = 0.01
            {
                "beta": [2.988, 1.72, 1.322, 1.075, 0.888, 0.732],
                "alpha": [0.132, 0.128, 0.118, 0.106, 0.092, 0.077],
            },
            # a'/a = 0.2
            {
                "beta": [1.72, 1.206, 1.024, 0.866, 0.729, 0.603],
                "alpha": [0.128, 0.124, 0.115, 0.103, 0.09, 0.075],
            },
            # a'/a = 0.4
            {
                "beta": [1.322, 1.024, 0.801, 0.694, 0.592, 0.492],
                "alpha": [0.118, 0.115, 0.107, 0.097, 0.084, 0.07],
            },
            # a'/a = 0.6
            {
                "beta": [1.075, 0.866, 0.694, 0.563, 0.483, 0.403],
                "alpha": [0.106, 0.103, 0.097, 0.087, 0.076, 0.064],
            },
            # a'/a = 0.8
            {
                "beta": [0.888, 0.729, 0.592, 0.483, 0.397, 0.331],
                "alpha": [0.092, 0.09, 0.084, 0.076, 0.066, 0.056],
            },
            # a'/a = 1
            {
                "beta": [0.732, 0.603, 0.492, 0.403, 0.331, 0.272],
                "alpha": [0.077, 0.075, 0.07, 0.064, 0.056, 0.047],
            },
        ],
        # bByA: 1.4
        [
            # a'/a = 0.01
            {
                "beta": [3.158, 1.501, 1.087, 0.824],
                "alpha": [0.169, 0.156, 0.133, 0.107],
            },
            # a'/a = 0.2
            {
                "beta": [1.683, 1.2, 0.925, 0.713],
                "alpha": [0.164, 0.153, 0.13, 0.105],
            },
            # a'/a = 0.4
            {
                "beta": [1.286, 0.968, 0.778, 0.61],
                "alpha": [0.153, 0.143, 0.122, 0.099],
            },
            # a'/a = 0.6
            {
                "beta": [1.042, 0.794, 0.654, 0.517],
                "alpha": [0.138, 0.129, 0.111, 0.09],
            },
            # a'/a = 0.8
            {
                "beta": [0.86, 0.656, 0.546, 0.435],
                "alpha": [0.12, 0.113, 0.097, 0.079],
            },
            # a'/a = 1
            {
                "beta": [0.708, 0.54, 0.451, 0.36],
                "alpha": [0.101, 0.095, 0.082, 0.066],
            },
        ],
        # bByA: 2
        [
            # a'/a = 0.01
            {
                "beta": [3.226, 1.587, 1.184, 0.942, 0.767, 0.628],
                "alpha": [0.188, 0.176, 0.155, 0.133, 0.112, 0.093],
            },
            # a'/a = 0.2
            {
                "beta": [1.636, 1.288, 1.023, 0.831, 0.683, 0.561],
                "alpha": [0.183, 0.172, 0.152, 0.13, 0.11, 0.091],
            },
            # a'/a = 0.4
            {
                "beta": [1.23, 1.051, 0.872, 0.721, 0.598, 0.492],
                "alpha": [0.171, 0.161, 0.143, 0.123, 0.104, 0.086],
            },
            # a'/a = 0.6
            {
                "beta": [1.01, 0.87, 0.739, 0.62, 0.517, 0.426],
                "alpha": [0.154, 0.146, 0.13, 0.112, 0.095, 0.079],
            },
            # a'/a = 0.8
            {
                "beta": [0.831, 0.723, 0.622, 0.525, 0.439, 0.363],
                "alpha": [0.134, 0.128, 0.114, 0.098, 0.083, 0.069],
            },
            # a'/a = 1
            {
                "beta": [0.684, 0.596, 0.515, 0.436, 0.365, 0.302],
                "alpha": [0.113, 0.107, 0.096, 0.083, 0.07, 0.058],
            },
        ],
    ]

    def _validate_edge_length(self, a: float, b: float) -> None:
        """
        エッジの長さのバリデーション
        
        Args:
            a: 短辺の長さ [mm]
            b: 長辺の長さ [mm]
            
        Raises:
            ValueError: 辺長比が計算係数テーブルの適用範囲外の場合
        """
        edge_length_ratio = b / a
        if edge_length_ratio < 1 or edge_length_ratio > 2:
            raise ValueError(
                "b/a is smaller than 1 or greater than 2. use FEM instead"
            )

    def _validate_a1_by_a(self, a1_by_a: float) -> None:
        """
        a1/a のバリデーション
        
        Args:
            a1_by_a: a1/a
            
        Raises:
            ValueError: a1/a が計算係数テーブルの適用範囲外の場合
        """
        if a1_by_a < 0.01 or a1_by_a > 1:
            raise ValueError(
                "a is greater than 1 or smaller than 0.01. use FEM instead"
            )

    def _validate_b1_by_a(self, b1_by_a: float, b1_by_a_list: List[float]) -> None:
        """
        b1/a のバリデーション
        
        Args:
            b1_by_a: b1/a
            b1_by_a_list: 係数テーブルに存在するb1/a のリスト
            
        Raises:
            ValueError: b1/a が計算係数テーブルの適用範囲外の場合
        """
        list_min = min(b1_by_a_list)
        list_max = max(b1_by_a_list)
        if b1_by_a < list_min or b1_by_a > list_max:
            raise ValueError(
                f"b1/a is smaller than {list_min} or greater than {list_max}. use FEM instead"
            )

    def _calculate_coeff(self) -> Dict[str, float]:
        """
        係数計算
        
        Returns:
            Dict[str, float]: 応力、変位計算用係数（alpha, beta）
            
        Raises:
            ValueError: 係数テーブルの適用範囲外の場合
        """
        b_by_a = self.edge_length_ratio
        a1_by_a = self.a1 / self.a
        b1_by_a = self.b1 / self.a
        tmp_bby_a_list = [1, 1.4, 2]
        tmp_a1by_a_list = [0.01, 0.2, 0.4, 0.6, 0.8, 1]
        tmp_b1by_a_list1 = [0.01, 0.2, 0.4, 0.6, 0.8, 1]
        tmp_b1by_a_list2 = [0.01, 0.4, 0.8, 1.2]
        tmp_b1by_a_list3 = [0.01, 0.4, 0.8, 1.2, 1.6, 2]

        index_bby_a = binary_search.binary_search(tmp_bby_a_list, b_by_a, BisectTypeEnum.LEFT)

        if index_bby_a == 0:
            tmp_b1by_a_list = tmp_b1by_a_list1
        elif index_bby_a == 1:
            tmp_b1by_a_list = tmp_b1by_a_list2
        elif index_bby_a == 2:
            tmp_b1by_a_list = tmp_b1by_a_list3
        else:
            raise ValueError("Invalid b/a ratio")

        self._validate_a1_by_a(a1_by_a)
        self._validate_b1_by_a(b1_by_a, tmp_b1by_a_list)

        index_a1by_a = binary_search.binary_search(tmp_a1by_a_list, a1_by_a, BisectTypeEnum.LEFT)
        index_b1by_a = binary_search.binary_search(tmp_b1by_a_list1, a1_by_a, BisectTypeEnum.LEFT)

        beta = self.coeff[index_bby_a][index_a1by_a]["beta"][index_b1by_a]
        alpha = self.coeff[index_bby_a][index_a1by_a]["alpha"][index_b1by_a]
        return {"alpha": alpha, "beta": beta}

    def calculate_stress(self) -> float:
        """
        応力計算
        
        Returns:
            float: 板の応力 [N/mm2]
        """
        thickness = self.layer.get_equivalent_thickness()
        sigma = (self.beta * (self.w * self.a1 * self.b1)) / thickness ** 2
        return sigma

    def calculate_displacement(self) -> float:
        """
        変位計算
        
        Returns:
            float: 板の変位 [mm]
        """
        thickness = self.layer.get_equivalent_thickness()
        e = self.material.E
        delta = (self.alpha * (self.w * self.a1 * self.b1 * self.a ** 2)) / (thickness ** 3 * e)
        return delta
