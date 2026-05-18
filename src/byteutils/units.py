"""Все единицы измерения объёма памяти"""

from enum import Enum
from typing import Dict

class Unit(Enum):
    """Единицы измерения памяти"""
    
    # Десятичные (основание 1000)
    B = "B"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"
    PB = "PB"
    EB = "EB"
    ZB = "ZB"
    YB = "YB"
    
    # Двоичные (основание 1024)
    KIB = "KiB"
    MIB = "MiB"
    GIB = "GiB"
    TIB = "TiB"
    PIB = "PiB"
    EIB = "EiB"
    ZIB = "ZiB"
    YIB = "YiB"
    
    # Стандарт JPYByte для ГИС
    IPY = "IPY"
    HPY = "HPY"
    GPY = "GPY"
    JPY = "JPY"


TO_BYTES: Dict[Unit, float] = {
    # Десятичные
    Unit.B: 1,
    Unit.KB: 1000,
    Unit.MB: 1000**2,
    Unit.GB: 1000**3,
    Unit.TB: 1000**4,
    Unit.PB: 1000**5,
    Unit.EB: 1000**6,
    Unit.ZB: 1000**7,
    Unit.YB: 1000**8,
    
    # Двоичные
    Unit.KIB: 1024,
    Unit.MIB: 1024**2,
    Unit.GIB: 1024**3,
    Unit.TIB: 1024**4,
    Unit.PIB: 1024**5,
    Unit.EIB: 1024**6,
    Unit.ZIB: 1024**7,
    Unit.YIB: 1024**8,
    
    # Стандарт JPYByte
    Unit.IPY: 2**90,
    Unit.HPY: 1000 * (2**90),
    Unit.GPY: 1000**2 * (2**90),
    Unit.JPY: 1000**3 * (2**90),
}

UNIT_NAMES: Dict[Unit, str] = {
    Unit.B: "байт",
    Unit.KB: "килобайт",
    Unit.MB: "мегабайт",
    Unit.GB: "гигабайт",
    Unit.TB: "терабайт",
    Unit.PB: "петабайт",
    Unit.EB: "эксабайт",
    Unit.ZB: "зеттабайт",
    Unit.YB: "йоттабайт",
    
    Unit.KIB: "кибибайт",
    Unit.MIB: "мебибайт",
    Unit.GIB: "гибибайт",
    Unit.TIB: "тебибайт",
    Unit.PIB: "пебибайт",
    Unit.EIB: "эксбибайт",
    Unit.ZIB: "зебибайт",
    Unit.YIB: "йобибайт",
    
    Unit.IPY: "айпибайт",
    Unit.HPY: "эйчпибайт",
    Unit.GPY: "джипибайт",
    Unit.JPY: "джейпибайт",
}
