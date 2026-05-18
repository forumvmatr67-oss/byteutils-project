"""Парсинг строк с размерами памяти"""

import re
from decimal import Decimal
from typing import Tuple, Union

from .units import Unit
from .converter import Converter


def parse_size(size_str: str, return_unit: bool = False) -> Union[Decimal, Tuple[Decimal, Unit]]:
    """
    Парсит строку с размером памяти и возвращает значение в байтах
    
    Поддерживаемые форматы:
        - "1.5 GB" / "1,5 GB" (десятичные)
        - "2 KiB" / "2 Киб" (двоичные)
        - "42 JPY" (шуточные)
        - "100 байт" / "5 килобайт" (русские названия)
        - "1.2гб" (без пробела)
    
    Args:
        size_str: Строка с размером (например, "2.5 MB")
        return_unit: Если True, возвращает кортеж (значение, единица)
    
    Returns:
        - Если return_unit=False: количество байт (Decimal)
        - Если return_unit=True: кортеж (значение в исходной единице, единица)
    
    Raises:
        ValueError: Если строка не может быть распарсена
        
    Примеры:
        >>> parse_size("2.5 MB")
        Decimal('2500000')
        
        >>> parse_size("1 KiB")
        Decimal('1024')
        
        >>> parse_size("42 JPY", return_unit=True)
        (Decimal('42'), <Unit.JPY: 'JPY'>)
        
        >>> parse_size("5 гигабайт")
        Decimal('5000000000')
    """
    
    # Регулярное выражение для поиска числа и единицы измерения
    # Поддерживает: цифры, точку, запятую, пробелы, русские и латинские буквы
    pattern = r'^([\d\.,]+)\s*([a-zA-Zа-яА-ЯiI]+)'
    match = re.match(pattern, size_str.strip())
    
    if not match:
        raise ValueError(f"Не удалось распарсить: {size_str}")
    
    num_str, unit_str = match.groups()
    
    # Преобразуем число (заменяем запятую на точку, убираем пробелы)
    num_str = num_str.replace(',', '.').replace(' ', '')
    value = Decimal(num_str)
    
    # Нормализуем единицу измерения
    unit = _normalize_unit(unit_str)
    
    if return_unit:
        return value, unit
    
    # Возвращаем в байтах
    return Converter.to_bytes(value, unit)


def _normalize_unit(unit_str: str) -> Unit:
    """
    Приводит строку с единицей измерения к стандартному виду Unit
    
    Args:
        unit_str: Строка с единицей измерения (например, "KB", "килобайт", "MiB")
    
    Returns:
        Соответствующая константа Unit
    
    Raises:
        ValueError: Если единица измерения не распознана
    """
    
    unit_str = unit_str.lower().strip()
    
    # Сопоставление различных вариантов написания с единицами
    mapping = {
        # ===== Десятичные (русские и английские) =====
        'b': Unit.B, 'байт': Unit.B, 'байта': Unit.B, 'байтов': Unit.B,
        'kb': Unit.KB, 'кб': Unit.KB, 'килобайт': Unit.KB,
        'mb': Unit.MB, 'мб': Unit.MB, 'мегабайт': Unit.MB,
        'gb': Unit.GB, 'гб': Unit.GB, 'гигабайт': Unit.GB,
        'tb': Unit.TB, 'тб': Unit.TB, 'терабайт': Unit.TB,
        'pb': Unit.PB, 'пб': Unit.PB, 'петабайт': Unit.PB,
        'eb': Unit.EB, 'эб': Unit.EB, 'эксабайт': Unit.EB,
        'zb': Unit.ZB, 'зб': Unit.ZB, 'зеттабайт': Unit.ZB,
        'yb': Unit.YB, 'йб': Unit.YB, 'йоттабайт': Unit.YB,
        
        # ===== Двоичные (русские и английские) =====
        'kib': Unit.KIB, 'киб': Unit.KIB, 'кибибайт': Unit.KIB,
        'mib': Unit.MIB, 'миб': Unit.MIB, 'мебибайт': Unit.MIB,
        'gib': Unit.GIB, 'гиб': Unit.GIB, 'гибибайт': Unit.GIB,
        'tib': Unit.TIB, 'тиб': Unit.TIB, 'тебибайт': Unit.TIB,
        'pib': Unit.PIB, 'пиб': Unit.PIB, 'пебибайт': Unit.PIB,
        'eib': Unit.EIB, 'эиб': Unit.EIB, 'эксбибайт': Unit.EIB,
        'zib': Unit.ZIB, 'зиб': Unit.ZIB, 'зебибайт': Unit.ZIB,
        'yib': Unit.YIB, 'йиб': Unit.YIB, 'йобибайт': Unit.YIB,
        
        # ===== Шуточные (русские и английские) =====
        'ipy': Unit.IPY, 'айпибайт': Unit.IPY,
        'hpy': Unit.HPY, 'эйчпибайт': Unit.HPY,
        'gpy': Unit.GPY, 'джипибайт': Unit.GPY,
        'jpy': Unit.JPY, 'джейпибайт': Unit.JPY,
    }
    
    if unit_str not in mapping:
        raise ValueError(f"Неизвестная единица измерения: {unit_str}")
    
    return mapping[unit_str]
