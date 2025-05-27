import math
from app.services.glass_calculator.material import Material
from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.contracts import InterlayerMaterialTypeEnum
from app.services.glass_calculator.circular.uniform import CircleUniformLoadGlass
from app.services.glass_calculator.threeside.uniform import ThreeSideUniformLoadGlass
from app.services.glass_calculator.twoside.uniform import TwoSideUniformLoadGlass
from app.services.glass_calculator.fourside.partial import FourSidePartialLoadGlass
from app.services.glass_calculator.fourside.uniform import FourSideUniformLoadGlass


class CalculateStress:

    @staticmethod
    def calculate_fourside_uniform(data):
        # 四辺支持板の計算式
        a = data.a  # mm
        b = data.b  # mm
        t = data.t  # mm
        w = data.w  # N/mm2
        nu = data.nu
        E = data.E
        material = Material(E, nu)
        layer = GlassLayer(t, InterlayerMaterialTypeEnum.SG) # type: ignore
        calculator = FourSideUniformLoadGlass(a, b, layer, w, material)
        sigma = calculator.calculate_stress()
        delta = calculator.calculate_displacement()
        return {"sigma": sigma, "delta": delta}

    @staticmethod
    def calculate_fourside_partial(data):
        # 四辺支持部分荷重板の計算式
        a = data.a  # mm
        b = data.b  # mm
        a1 = data.a1  # mm
        b1 = data.b1  # mm
        t = data.t  # mm
        w = data.w  # N/mm2
        E = data.E
        nu = data.nu
        material = Material(E, nu)
        layer = GlassLayer(t, InterlayerMaterialTypeEnum.SG) # type: ignore
        calculator = FourSidePartialLoadGlass(a, b, layer, w, a1, b1, material)
        sigma = calculator.calculate_stress()
        delta = calculator.calculate_displacement()

        return {"sigma": round(sigma, 2), "delta": round(delta, 2)}

    @staticmethod
    def calculate_threeside_uniform(data):
        # 三辺支持板の計算式
        a = data.free  # mm
        b = data.fix  # mm
        t = data.t  # mm -> m
        w = data.w  # N/mm2
        nu = data.nu
        E = data.E
        material = Material(E, nu)
        layer = GlassLayer(t, InterlayerMaterialTypeEnum.SG) # type: ignore
        calculator = ThreeSideUniformLoadGlass(a, b, layer, w, material)
        sigma = calculator.calculate_stress()
        delta = calculator.calculate_displacement()

        return {"sigma": round(sigma, 2), "delta": round(delta, 2)}

    @staticmethod
    def calculate_twoside_uniform(data):
        # 二辺支持板の計算式
        a = data.free  # mm
        b = data.fix  # mm
        t = data.t  # mm -> m
        w = data.w  # N/mm2
        nu = data.nu
        E = data.E
        material = Material(E, nu)
        layer = GlassLayer(t, InterlayerMaterialTypeEnum.SG) # type: ignore
        calculator = TwoSideUniformLoadGlass(a, b, layer, w, material)
        sigma = calculator.calculate_stress()
        delta = calculator.calculate_displacement()

        return {"sigma": round(sigma, 2), "delta": round(delta, 2)}

    @staticmethod
    def calculate_circular_uniform(data):
        # 円形支持板の計算式
        r = data.D / 2  # mm
        t = data.t  # mm -> m
        w = data.w  # N/mm2
        nu = data.nu
        E = data.E
        material = Material(E, nu)
        layer = GlassLayer(t, InterlayerMaterialTypeEnum.SG) # type: ignore
        calculator = CircleUniformLoadGlass(r, layer, w, material)
        sigma = calculator.calculate_stress()
        delta = calculator.calculate_displacement()

        return {"sigma": round(sigma, 2), "delta": round(delta, 2)}
