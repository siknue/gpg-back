from app.services.glass_calculator.glass_material import GlassMaterial
from app.services.glass_calculator.glass_layer import GlassLayer


class CircleUniformLoadGlass:
    """
    CircleSupportedUniformLoadGlass class
    Calculates stress and displacement for a circular glass plate under uniform load.
    """
    
    def __init__(self, radius: float, layer: GlassLayer, w: float, material:GlassMaterial):
        """
        Constructor
        
        Args:
            radius: Radius of the circular plate [mm]
            layer: Glass layer object
            w: Load [N/mm²]
            material: マテリアル
        """
        self.radius = radius
        self.layer = layer
        self.w = w
        self.constants = material
    
    def calculate_stress(self) -> float:
        """
        Calculate stress on the circular plate
        
        Returns:
            float: Stress on the plate [N/mm²]
        """
        thickness = self.layer.get_equivalent_thickness()
        sigma = 1.212 * (self.w * self.radius**2) / thickness**2
        print(f"1.212 * ({self.w} * {self.radius}**2) / {thickness}**2")
        return sigma
    
    def calculate_displacement(self) -> float:
        """
        Calculate displacement of the circular plate
        
        Returns:
            float: Displacement of the plate [mm]
        """
        e = self.constants.E
        thickness = self.layer.get_equivalent_thickness()
        delta = 0.756 * (self.w * self.radius**4) / (e * thickness**3)
        return delta
