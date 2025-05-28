import pytest
from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.contracts.enums import InterlayerMaterialTypeEnum
from app.services.glass_calculator.fourside.uniform import FourSideUniformLoadGlass
from app.services.glass_calculator.glass_material import GlassMaterial


class TestFourSideUniformLoadGlass:
    """四辺支持された均一荷重下のガラス板のテスト"""

    class TestConstructor:
        """コンストラクタのテスト"""

        def test_valid_parameters(self):
            """正常なパラメータでインスタンスが生成されること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            test_glass = FourSideUniformLoadGlass(
                100, 200, glass_layer, 1.0, glass_material
            )

            assert isinstance(test_glass, FourSideUniformLoadGlass)
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

            with pytest.raises(
                ValueError, match="短辺が長辺より長くなることはできません"
            ):
                FourSideUniformLoadGlass(200, 100, glass_layer, 1.0, glass_material)

        def test_edge_length_ratio_exceeds_maximum(self):
            """辺長比が最大値より大きい場合にエラーが発生すること"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()

            with pytest.raises(
                ValueError, match="b/aが5を超えています。代わりにFEMを使用してください"
            ):
                FourSideUniformLoadGlass(
                    100, 600, glass_layer, 1.0, glass_material
                )  # b/a = 6

    class TestCalculateCoeff:
        """係数計算メソッドのテスト"""

        def test_coefficients_for_edge_ratio_1(self):
            """辺長比に基づいて適切な係数を取得できること (b/a = 1)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSideUniformLoadGlass(100, 100, glass_layer, 1.0, glass_material)

            # プライベートメソッドにアクセス
            coeff = plate._calculate_coeff()

            assert pytest.approx(coeff["alpha"], 0.001) == 0.047
            assert pytest.approx(coeff["beta"], 0.001) == 0.272

        def test_coefficients_for_edge_ratio_2(self):
            """辺長比に基づいて適切な係数を取得できること (b/a = 2)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSideUniformLoadGlass(100, 200, glass_layer, 1.0, glass_material)

            coeff = plate._calculate_coeff()

            assert pytest.approx(coeff["alpha"], 0.001) == 0.116
            assert pytest.approx(coeff["beta"], 0.001) == 0.603

        def test_coefficients_for_edge_ratio_5(self):
            """辺長比に基づいて適切な係数を取得できること (b/a = 5)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSideUniformLoadGlass(100, 500, glass_layer, 1.0, glass_material)

            coeff = plate._calculate_coeff()

            assert pytest.approx(coeff["alpha"], 0.001) == 0.148
            assert pytest.approx(coeff["beta"], 0.001) == 0.748

    class TestCalculateStress:
        """応力計算メソッドのテスト"""

        def test_stress_calculation_for_edge_ratio_1(self):
            """応力を計算できること (b/a = 1)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSideUniformLoadGlass(100, 100, glass_layer, 1.0, glass_material)

            stress = plate.calculate_stress()

            # thickness.get_equivalent_thickness() は 12 を返すと仮定
            expected = (0.272 * (1.0 * 100**2)) / 144
            assert pytest.approx(stress, 0.001) == expected

        def test_stress_calculation_for_edge_ratio_2(self):
            """応力を計算できること (b/a = 2)"""
            layer = [5]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSideUniformLoadGlass(
                100, 200, glass_layer, 0.5, glass_material  # w を変更
            )

            stress = plate.calculate_stress()

            # thickness.get_equivalent_thickness() は 5 を返すと仮定
            expected = (0.603 * (0.5 * 100**2)) / 25
            assert pytest.approx(stress, 0.001) == expected

    class TestCalculateDisplacement:
        """変位計算メソッドのテスト"""

        def test_displacement_calculation_for_edge_ratio_1(self):
            """変位を計算できること (b/a = 1)"""
            layer = [6, 6]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSideUniformLoadGlass(100, 100, glass_layer, 1.0, glass_material)

            displacement = plate.calculate_displacement()

            E = plate.material.E
            # thickness**3 は 1728 (12^3)
            expected = (0.047 * (1.0 * 100**4)) / (1728 * E)
            assert pytest.approx(displacement, 0.001) == expected

        def test_displacement_calculation_for_edge_ratio_2(self):
            """変位を計算できること (b/a = 2)"""
            layer = [5]
            inter_layer_material = InterlayerMaterialTypeEnum.SG
            glass_layer = GlassLayer(layer, inter_layer_material) # type: ignore
            glass_material = GlassMaterial()
            plate = FourSideUniformLoadGlass(
                100, 200, glass_layer, 0.5, glass_material  # w を変更
            )

            displacement = plate.calculate_displacement()

            E = plate.material.E
            # thickness**3 は 125 (5^3)
            expected = (0.116 * (0.5 * 100**4)) / (125 * E)
            assert pytest.approx(displacement, 0.001) == expected
