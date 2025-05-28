import pytest
from app.services.glass_calculator.glass_material import GlassMaterial
from app.services.glass_calculator.circular.uniform import CircleUniformLoadGlass
from app.services.glass_calculator.contracts.enums import InterlayerMaterialTypeEnum
from app.services.glass_calculator.glass_layer import GlassLayer


class TestCircleSupportedUniformLoadGlass:
    """円形支持均等荷重ガラスの計算クラスのテスト"""
    
    class TestConstructor:
        """コンストラクタのテスト"""
        
        def test_valid_parameters(self):
            """正常なパラメータでインスタンスが生成されること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            material = GlassMaterial()
            test_glass = CircleUniformLoadGlass(
                1000,
                glass_layer,
                1.0,
                material
            )
            
            assert isinstance(test_glass, CircleUniformLoadGlass)
            assert test_glass.radius == 1000
            assert test_glass.layer == glass_layer
            assert test_glass.w == 1.0
    
    class TestCalculateStress:
        """応力計算メソッドのテスト"""
        
        def test_stress_calculation(self):
            """応力を計算できること"""
            layer_thickness = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer_thickness, inter_layer_material) # type: ignore
            print(glass_layer.get_equivalent_thickness())
            glass_material = GlassMaterial()
            plate = CircleUniformLoadGlass(
                500,
                glass_layer,
                1.0,
                glass_material
            )
            
            stress = plate.calculate_stress()
            
            # thickness.get_equivalent_thickness() は 12 を返すと仮定
            expected = 1.212 * (1 * 500**2) / 12**2
            assert pytest.approx(stress, 0.001) == expected
    
    class TestCalculateDisplacement:
        """変位計算メソッドのテスト"""
        
        def test_displacement_calculation(self):
            """変位を計算できること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = CircleUniformLoadGlass(
                500,
                glass_layer,
                1.0,
                glass_material
            )
            
            displacement = plate.calculate_displacement()
            
            E = plate.constants.E
            # thickness**3 は 1728 (12^3)
            expected = 0.756 * (1 * 500**4) / (E * 12**3)
            assert pytest.approx(displacement, 0.001) == expected
