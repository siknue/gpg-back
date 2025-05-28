from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.contracts.enums import InterlayerMaterialTypeEnum
from app.services.glass_calculator.fourside.partial import FourSidePartialLoadGlass
import pytest

from app.services.glass_calculator.glass_material import GlassMaterial

class TestFourSidePartialLoadGlass:
    """四辺支持部分均等荷重ガラス計算クラスのテスト"""
    
    class TestConstructor:
        """コンストラクタのテスト"""
        
        def test_valid_parameters(self):
            """正常なパラメータでインスタンスが生成されること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            test_glass = FourSidePartialLoadGlass(
                100,
                200,
                glass_layer,
                1.0,
                80,
                160,
                glass_material
            )
            
            assert isinstance(test_glass, FourSidePartialLoadGlass)
            assert test_glass.a == 100
            assert test_glass.b == 200
            assert test_glass.edge_length_ratio == 2
            assert test_glass.layer == glass_layer
            assert test_glass.w == 1.0
        
        def test_shorter_edge_greater_than_longer_edge(self):
            """短い辺が長い辺より大きい場合にエラーが発生すること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            
            with pytest.raises(ValueError, match="b/a is smaller than 1 or greater than 2. use FEM instead"):
                FourSidePartialLoadGlass(
                    201,
                    200,
                    glass_layer,
                    1.0,
                    80,
                    160,
                    glass_material
                )
        
        def test_edge_length_ratio_exceeds_maximum(self):
            """辺長比が最大値より大きい場合にエラーが発生すること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            with pytest.raises(ValueError, match="b/a is smaller than 1 or greater than 2. use FEM instead"):
                FourSidePartialLoadGlass(
                    100,
                    201,
                    glass_layer,
                    1.0,
                    80,
                    160,
                    glass_material
                )  # b/a > 2
    
    class TestCalculateCoeff:
        """係数計算メソッドのテスト"""
        
        def test_coefficients_for_edge_ratio_1_a1_ratio_001_b1_ratio_001(self):
            """辺長比に基づいて適切な係数を取得できること (b/a = 1)(a1/a = 0.01)(b1/a = 0.01)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSidePartialLoadGlass(
                1000,
                1000,
                glass_layer,
                1.0,
                10,
                10,
                glass_material
            )
            
            # プライベートメソッドにアクセス
            coeff = plate._calculate_coeff()
            
            assert pytest.approx(coeff["alpha"], 0.001) == 0.132
            assert pytest.approx(coeff["beta"], 0.001) == 2.988
        
        def test_coefficients_for_edge_ratio_2_a1_ratio_001_b1_ratio_001(self):
            """辺長比に基づいて適切な係数を取得できること (b/a = 2)(a1/a = 0.01)(b1/a = 0.01)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSidePartialLoadGlass(
                1000,
                2000,
                glass_layer,
                1.0,
                10,
                20,
                glass_material
            )
            
            # プライベートメソッドにアクセス
            coeff = plate._calculate_coeff()
            
            assert pytest.approx(coeff["alpha"], 0.001) == 0.188
            assert pytest.approx(coeff["beta"], 0.001) == 3.226
    
    class TestCalculateStress:
        """応力計算メソッドのテスト"""
        
        def test_stress_calculation_for_edge_ratio_1(self):
            """応力を計算できること (b/a = 1)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSidePartialLoadGlass(
                1000,
                1000,
                glass_layer,
                1.0,
                10,
                10,
                glass_material
            )
            
            stress = plate.calculate_stress()
            
            expected = 2.988 * (1 * 10 * 10) / (12**2)
            assert pytest.approx(stress, 0.001) == expected
        
        def test_stress_calculation_for_edge_ratio_2(self):
            """応力を計算できること (b/a = 2)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSidePartialLoadGlass(
                1000,
                2000,
                glass_layer,
                1.0,
                10,
                20,
                glass_material
            )
            
            stress = plate.calculate_stress()
            
            expected = 3.226 * (1 * 10 * 20) / (12**2)
            assert pytest.approx(stress, 0.001) == expected
    
    class TestCalculateDisplacement:
        """変位計算メソッドのテスト"""
        
        def test_displacement_calculation_for_edge_ratio_1(self):
            """変位を計算できること (b/a = 1)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSidePartialLoadGlass(
                1000,
                1000,
                glass_layer,
                1.0,
                10,
                10,
                glass_material
            )
            
            displacement = plate.calculate_displacement()
            
            expected = 0.132 * (1 * 10 * 10 * 1000**2) / (71600 * 12**3)
            assert pytest.approx(displacement, 0.001) == expected
        
        def test_displacement_calculation_for_edge_ratio_2(self):
            """変位を計算できること (b/a = 2)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSidePartialLoadGlass(
                1000,
                2000,
                glass_layer,
                1.0,
                10,
                20,
                glass_material
            )
            
            displacement = plate.calculate_displacement()
            
            expected = 0.188 * (1 * 10 * 20 * 1000**2) / (71600 * 12**3)
            assert pytest.approx(displacement, 0.001) == expected
