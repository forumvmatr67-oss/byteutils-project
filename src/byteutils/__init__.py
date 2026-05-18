"""
byteutils - универсальная библиотека для работы с единицами измерения памяти

Поддерживаемые единицы:
- Десятичные: B, KB, MB, GB, TB, PB, EB, ZB, YB
- Двоичные: KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB
- Шуточные: IPY, HPY, GPY, JPY

Примеры:
    >>> from byteutils import format_size, Converter, Unit
    >>> format_size(1234567890)
    '1.23 GB'
    >>> Converter.convert(1, Unit.GB, Unit.MB)
    Decimal('1000')
    >>> parse_size("2.5 MB")
    Decimal('2500000')
"""

from .units import Unit, TO_BYTES, UNIT_NAMES
from .converter import Converter
from .formatter import format_size
from .parser import parse_size
from .auto_detect import best_unit, best_format

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"
__all__ = [
    "Unit",
    "TO_BYTES", 
    "UNIT_NAMES",
    "Converter",
    "format_size",
    "parse_size",
    "best_unit",
    "best_format",
]
