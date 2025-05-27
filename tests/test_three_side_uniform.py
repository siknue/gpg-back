from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.contracts import InterlayerMaterialTypeEnum
from app.services.glass_calculator.material import Material
from app.services.glass_calculator.threeside.uniform import ThreeSideUniformLoadGlass
import pytest


class TestThreeSideUniformLoadGlass:
    """三辺支持された均一荷重下のガラス板のテスト"""
    
    class TestConstructor:
        """コンストラクタのテスト"""
        
        def test_valid_parameters(self):
            """正常なパラメータでインスタンスが生成されること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            test_glass = ThreeSideUniformLoadGlass(
                100,
                200,
                glass_layer,
                1.0,
                glass_material
            )
            
            assert isinstance(test_glass, ThreeSideUniformLoadGlass)
            assert test_glass.a == 100
            assert test_glass.b == 200
            assert test_glass.edge_length_ratio == 2
            assert test_glass.layer == glass_layer
            assert test_glass.w == 1.0
        
        def test_fixed_edge_ratio_too_small(self):
            """固定辺/フリー < 0.1 の場合にエラーが発生すること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            
            with pytest.raises(ValueError, match="b/a is smaller than 0.1. use FEM instead"):
                ThreeSideUniformLoadGlass(1001, 100, glass_layer, 1.0, glass_material)
    
    class TestCalculateCoeff:
        """係数計算メソッドのテスト"""
        
        def test_coefficients_for_edge_ratio_0_1(self):
            """辺長比に基づいて適切な係数を取得できること (b/a = 0.1)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            plate = ThreeSideUniformLoadGlass(
                1000,
                100,
                glass_layer,
                1.0,
                glass_material
            )
            
            # プライベートメソッドにアクセス
            coeff = plate._calculate_coeff()
            
            assert pytest.approx(coeff["alpha"], 0.001) == 0.005
            assert pytest.approx(coeff["beta"], 0.001) == 0.071
        
        def test_coefficients_for_edge_ratio_2(self):
            """辺長比に基づいて適切な係数を取得できること (b/a = 2)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            plate = ThreeSideUniformLoadGlass(
                1000,
                3000,
                glass_layer,
                1.0,
                glass_material
            )
            
            coeff = plate._calculate_coeff()
            
            assert pytest.approx(coeff["alpha"], 0.001) == 0.165
            assert pytest.approx(coeff["beta"], 0.001) == 0.791
        
        def test_coefficients_for_edge_ratio_greater_than_3(self):
            """辺長比に基づいて適切な係数を取得できること (b/a >3)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            plate = ThreeSideUniformLoadGlass(
                100,
                500,
                glass_layer,
                1.0,
                glass_material
            )
            
            coeff = plate._calculate_coeff()
            
            assert pytest.approx(coeff["alpha"], 0.001) == 0.165
            assert pytest.approx(coeff["beta"], 0.001) == 0.791
    
    class TestCalculateStress:
        """応力計算メソッドのテスト"""
        
        def test_stress_calculation_for_edge_ratio_0_1(self):
            """応力を計算できること (b/a = 0.1)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            plate = ThreeSideUniformLoadGlass(
                1000,
                100,
                glass_layer,
                1.0,
                glass_material
            )
            
            stress = plate.calculate_stress()
            
            # thickness.get_equivalent_thickness() は 12 を返すと仮定
            expected = (0.071 * (1.0 * 1000 ** 2)) / 144
            assert pytest.approx(stress, 0.001) == expected
        
        def test_stress_calculation_for_edge_ratio_greater_than_3(self):
            """応力を計算できること (b/a > 3)"""
            layer = [5]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            plate = ThreeSideUniformLoadGlass(
                100,
                300,
                glass_layer,
                1.0,
                glass_material
            )
            
            stress = plate.calculate_stress()
            
            # thickness.get_equivalent_thickness() は 5 を返すと仮定
            expected = (0.791 * (1.0 * 100 ** 2)) / 25
            assert pytest.approx(stress, 0.001) == expected
    
    class TestCalculateDisplacement:
        """変位計算メソッドのテスト"""
        
        def test_displacement_calculation_for_edge_ratio_0_1(self):
            """変位を計算できること (b/a = 0.1)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            plate = ThreeSideUniformLoadGlass(
                1000,
                100,
                glass_layer,
                1.0,
                glass_material
            )
            
            displacement = plate.calculate_displacement()
            
            E = plate.material.E
            # thickness**3 は 1728 (12^3)
            expected = (0.005 * (1.0 * 1000 ** 4)) / (1728 * E)
            assert pytest.approx(displacement, 0.001) == expected
        
        def test_displacement_calculation_for_edge_ratio_greater_than_3(self):
            """変位を計算できること (b/a > 3)"""
            layer = [5]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = Material()
            plate = ThreeSideUniformLoadGlass(
                100,
                300,
                glass_layer,
                1,
                glass_material
            )
            
            displacement = plate.calculate_displacement()
            
            E = plate.material.E
            # thickness**3 は 125 (5^3)
            expected = (0.165 * (1 * 100 ** 4)) / (125 * E)
            assert pytest.approx(displacement, 0.001) == expected
