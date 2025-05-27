from app.services.glass_calculator.glass_layer import GlassLayer
from app.services.glass_calculator.contracts import AllowableStressTerms, FractureStrength, GlassTypeEnum, IAllowableStress, StressLimits

class GlassAllowableUnitStress:
    def __init__(self, glass_layer: GlassLayer, glass_type: GlassTypeEnum):
        self.glass_layer = glass_layer
        self.glass_type = glass_type
        self.allowable_stress = self.calculate_allowable_stress()
    
    # データベースは大規模なので、クラス変数として定義
    allowable_stress_db = {
        GlassTypeEnum.FLOAT: {
            "t<=8": {
                "fracturesStrength": {
                    "inplane": 54.9,
                    "edge": 35.3,
                },
                "allowableStress": {
                    "shortTerm": {
                        "inplane": 24.5,
                        "edge": 17.7,
                    },
                    "longTerm": {
                        "inplane": 9.8,
                        "edge": 6.9,
                    },
                },
            },
            "8<t<=12": {
                "fracturesStrength": {
                    "inplane": 51.5,
                    "edge": 35.3,
                },
                "allowableStress": {
                    "shortTerm": {
                        "inplane": 22.1,
                        "edge": 17.7,
                    },
                    "longTerm": {
                        "inplane": 8.8,
                        "edge": 6.9,
                    },
                },
            },
            "12<t<=20": {
                "fracturesStrength": {
                    "inplane": 48.1,
                    "edge": 35.3,
                },
                "allowableStress": {
                    "shortTerm": {
                        "inplane": 19.6,
                        "edge": 17.7,
                    },
                    "longTerm": {
                        "inplane": 7.8,
                        "edge": 6.9,
                    },
                },
            },
            "t>20": {
                "fracturesStrength": {
                    "inplane": 46.6,
                    "edge": 35.3,
                },
                "allowableStress": {
                    "shortTerm": {
                        "inplane": 18.6,
                        "edge": 17.7,
                    },
                    "longTerm": {
                        "inplane": 7.4,
                        "edge": 6.9,
                    },
                },
            },
        },
        GlassTypeEnum.WIRED: {
            "6<=t<=10": {
                "fracturesStrength": {
                    "inplane": 36.8,
                    "edge": 19.6,
                },
                "allowableStress": {
                    "shortTerm": {
                        "inplane": 19.6,
                        "edge": 9.8,
                    },
                    "longTerm": {
                        "inplane": 7.8,
                        "edge": 3.9,
                    },
                },
            },
        },
        GlassTypeEnum.WIRE_PATTERNED: {
            "6<=t<=8": {
                "fracturesStrength": {
                    "inplane": 29.4,
                    "edge": 19.6,
                },
                "allowableStress": {
                    "shortTerm": {
                        "inplane": 14.7,
                        "edge": 9.8,
                    },
                    "longTerm": {
                        "inplane": 5.9,
                        "edge": 3.9,
                    },
                },
            },
        },
        GlassTypeEnum.TEMPERED: {
            "4<=t<=19": {
                "fracturesStrength": {
                    "inplane": 142.2,
                    "edge": 131.4,
                },
                "allowableStress": {
                    "shortTerm": {
                        "inplane": 88.3,
                        "edge": 79.4,
                    },
                    "longTerm": {
                        "inplane": 73.5,
                        "edge": 68.6,
                    },
                },
            },
        },
        GlassTypeEnum.DOUBLE: {
            "6<=t<=12": {
                "fracturesStrength": {
                    "inplane": 78.5,
                    "edge": 70.6,
                },
                "allowableStress": {
                    "shortTerm": {
                        "inplane": 44.1,
                        "edge": 35.3,
                    },
                    "longTerm": {
                        "inplane": 29.4,
                        "edge": 24.5,
                    },
                },
            },
        },
    }

    def calculate_allowable_stress(self) -> IAllowableStress:
        """
        ガラスの許容応力値を計算する
        
        Returns:
            IAllowableStress: 許容応力値のオブジェクト
        
        Raises:
            ValueError: 無効なガラスタイプまたは厚さの場合
        """
        outer_thickness = min(self.glass_layer.get_outer_layer_thickness())
        allowable_stress = None

        if self.glass_type == GlassTypeEnum.FLOAT:
            if outer_thickness <= 8:
                allowable_stress = self.allowable_stress_db[GlassTypeEnum.FLOAT]["t<=8"]
            elif 8 < outer_thickness <= 12:
                allowable_stress = self.allowable_stress_db[GlassTypeEnum.FLOAT]["8<t<=12"]
            elif 12 < outer_thickness <= 20:
                allowable_stress = self.allowable_stress_db[GlassTypeEnum.FLOAT]["12<t<=20"]
            elif outer_thickness > 20:
                allowable_stress = self.allowable_stress_db[GlassTypeEnum.FLOAT]["t>20"]
                
        elif self.glass_type == GlassTypeEnum.WIRED:
            if 6 <= outer_thickness <= 10:
                allowable_stress = self.allowable_stress_db[GlassTypeEnum.WIRED]["6<=t<=10"]
            else:
                raise ValueError(f"無効なガラスタイプまたは厚さ: {self.glass_type}, {outer_thickness}")
                
        elif self.glass_type == GlassTypeEnum.WIRE_PATTERNED:
            if 6 <= outer_thickness <= 8:
                allowable_stress = self.allowable_stress_db[GlassTypeEnum.WIRE_PATTERNED]["6<=t<=8"]
                
        elif self.glass_type == GlassTypeEnum.TEMPERED:
            if 4 <= outer_thickness <= 19:
                allowable_stress = self.allowable_stress_db[GlassTypeEnum.TEMPERED]["4<=t<=19"]
                
        elif self.glass_type == GlassTypeEnum.DOUBLE:
            if 6 <= outer_thickness <= 12:
                allowable_stress = self.allowable_stress_db[GlassTypeEnum.DOUBLE]["6<=t<=12"]
                
        if allowable_stress is None:
            raise ValueError(f"無効なガラスタイプまたは厚さ: {self.glass_type}, {outer_thickness}")
            
        # 辞書からIAllowableStressオブジェクトに変換
        fracturesStrength = FractureStrength(
            inplane=allowable_stress["fracturesStrength"]["inplane"],
            edge=allowable_stress["fracturesStrength"]["edge"]
        )
        
        shortTerm = StressLimits(
            inplane=allowable_stress["allowableStress"]["shortTerm"]["inplane"],
            edge=allowable_stress["allowableStress"]["shortTerm"]["edge"]
        )
        
        longTerm = StressLimits(
            inplane=allowable_stress["allowableStress"]["longTerm"]["inplane"],
            edge=allowable_stress["allowableStress"]["longTerm"]["edge"]
        )
        
        return IAllowableStress(
            fracturesStrength=fracturesStrength,
            allowableStress=AllowableStressTerms(
                shortTerm=shortTerm,
                longTerm=longTerm
            )
        )

    def check_stress(self, stress: float) -> float:
        """
        応力値をチェックする
        
        Args:
            stress: チェックする応力値
            
        Returns:
            float: 有効な応力値
            
        Raises:
            ValueError: 圧縮応力をチェックしようとした場合
        """
        if stress < 0:
            raise ValueError("圧縮応力のチェックは許可されていません")
        else:
            return stress