import math

from app.services.glass_calculator.contracts.enums import InterlayerMaterialTypeEnum, GlassTypeEnum

from app.services.glass_calculator.glass_material import GlassMaterial
from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.circular.uniform import CircleUniformLoadGlass
from app.services.glass_calculator.threeside.uniform import ThreeSideUniformLoadGlass
from app.services.glass_calculator.twoside.uniform import TwoSideUniformLoadGlass
from app.services.glass_calculator.fourside.partial import FourSidePartialLoadGlass
from app.services.glass_calculator.fourside.uniform import FourSideUniformLoadGlass
from app.services.glass_calculator.allowable_stress import GlassAllowableUnitStress
from typing import Sequence
class CalculateStress:

    @staticmethod
    def calculate_fourside_uniform(data):
        try:
            # 四辺支持板の計算式
            a = data.a  # mm
            b = data.b  # mm
            glass_layer_thicknesses = data.t  # mm list of thicknesses
            w = data.w  # N/mm2
            nu = data.nu
            E = data.E
            #inter_layer_material = data.interlayer_material  # InterlayerMaterialTypeEnum

            glass_material = GlassMaterial(E, nu)
            glass_layer = GlassLayer(glass_layer_thicknesses, InterlayerMaterialTypeEnum.SG) # type: ignore
            calculator = FourSideUniformLoadGlass(a, b, glass_layer, w, glass_material)
            sigma = calculator.calculate_stress()
            delta = calculator.calculate_displacement()

            # 許容応力度の計算
            glass_type = GlassTypeEnum.FLOAT  # ガラスの種類を指定
            allowabe_stress_calculator = GlassAllowableUnitStress(glass_layer, glass_type)
            #print(f"allowable_stress: {allowabe_stress_calculator.allowable_stress.allowableStress.shortTerm.edge}")

            return {"sigma": round(sigma, 2), "delta": round(delta, 2)}
        except ValueError as e:
            return {"error": str(e)}

    @staticmethod
    def calculate_fourside_partial(data):
        try:
            # 四辺支持部分荷重板の計算式
            a = data.a  # mm
            b = data.b  # mm
            a1 = data.a1  # mm
            b1 = data.b1  # mm
            glass_layer_thicknesses = data.t  # mm
            w = data.w  # N/mm2
            E = data.E
            nu = data.nu
            material = GlassMaterial(E, nu)
            layer = GlassLayer(glass_layer_thicknesses, InterlayerMaterialTypeEnum.SG) # type: ignore
            calculator = FourSidePartialLoadGlass(a, b, layer, w, a1, b1, material)
            sigma = calculator.calculate_stress()
            delta = calculator.calculate_displacement()

            return {"sigma": round(sigma, 2), "delta": round(delta, 2)}
        except ValueError as e:
            return {"error": str(e)}

    @staticmethod
    def calculate_threeside_uniform(data):
        try:
            # 三辺支持板の計算式
            a = data.free  # mm
            b = data.fix  # mm
            glass_layer_thicknesses = data.t  # mm -> m
            w = data.w  # N/mm2
            nu = data.nu
            E = data.E
            material = GlassMaterial(E, nu)
            layer = GlassLayer(glass_layer_thicknesses, InterlayerMaterialTypeEnum.SG) # type: ignore
            calculator = ThreeSideUniformLoadGlass(a, b, layer, w, material)
            sigma = calculator.calculate_stress()
            delta = calculator.calculate_displacement()

            return {"sigma": round(sigma, 2), "delta": round(delta, 2)}
        except ValueError as e:
            return {"error": str(e)}

    @staticmethod
    def calculate_twoside_uniform(data):
        try:
            # 二辺支持板の計算式
            a = data.free  # mm
            b = data.fix  # mm
            glass_layer_thicknesses = data.t  # mm -> m
            w = data.w  # N/mm2
            nu = data.nu
            E = data.E
            material = GlassMaterial(E, nu)
            layer = GlassLayer(glass_layer_thicknesses, InterlayerMaterialTypeEnum.SG) # type: ignore
            calculator = TwoSideUniformLoadGlass(a, b, layer, w, material)
            sigma = calculator.calculate_stress()
            delta = calculator.calculate_displacement()

            return {"sigma": round(sigma, 2), "delta": round(delta, 2)}
        except ValueError as e:
            return {"error": str(e)}

    @staticmethod
    def calculate_circular_uniform(data):
        try:
            # 円形支持板の計算式
            r = data.D / 2  # mm
            glass_layer_thicknesses = data.t  # mm -> m
            w = data.w  # N/mm2
            nu = data.nu
            E = data.E
            material = GlassMaterial(E, nu)
            layer = GlassLayer(glass_layer_thicknesses, InterlayerMaterialTypeEnum.SG) # type: ignore
            calculator = CircleUniformLoadGlass(r, layer, w, material)
            sigma = calculator.calculate_stress()
            delta = calculator.calculate_displacement()

            return {"sigma": round(sigma, 2), "delta": round(delta, 2)}
        except ValueError as e:
            return {"error": str(e)}
