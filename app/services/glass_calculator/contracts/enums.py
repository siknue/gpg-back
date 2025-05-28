from enum import Enum


class GlassTypeEnum(Enum):
    FLOAT = "float"
    WIRED = "wired"
    WIRE_PATTERNED = "wirePatterend"
    TEMPERED = "tempered"
    DOUBLE = "double"

class InterlayerMaterialTypeEnum(Enum):
    SG = "sg"
    PVB = "pvb"
    EVA = "eva"