"""Автоматическое определение оптимальной единицы измерения"""

from typing import Optional, Union
from decimal import Decimal

from .units import Unit, TO_BYTES
from .converter import Converter
from .formatter import format_size


def best_unit(
    bytes_val: Union[int, float, Decimal],
    binary: bool = False,
    max_unit: Optional[Unit] = None,
    min_value: float = 1.0
) -> Unit:
    """
    Выбирает оптимальную единицу измерения для заданного количества байт
    
    Алгоритм:
        1. Пытается найти единицу, в которой значение >= min_value
        2. Использует самые большие возможные единицы
        3. Для огромных чисел подключает шуточные единицы (IPY, HPY, GPY, JPY)
    
    Args:
        bytes_val: Количество байт
        binary: Использовать двоичные единицы (KiB, MiB...) вместо десятичных
        max_unit: Максимально допустимая единица (не выше этой)
        min_value: Минимальное значение в выбранной единице (по умолчанию >=1)
    
    Returns:
        Оптимальная единица измерения
        
    Примеры:
        >>> best_unit(500)
        <Unit.B: 'B'>
        
        >>> best_unit(1500)
        <Unit.KB: 'KB'>
        
        >>> best_unit(1500, binary=True)
        <Unit.KIB: 'KiB'>
        
        >>> best_unit(1_500_000_000)
        <Unit.GB: 'GB'>
        
        >>> best_unit(10**30)
        <Unit.JPY: 'JPY'>
    """
    
    bytes_dec = Decimal(str(bytes_val))
    
    # Базовый список единиц в порядке возрастания
    if binary:
        units = [Unit.B, Unit.KIB, Unit.MIB, Unit.GIB, Unit.TIB, 
                 Unit.PIB, Unit.EIB, Unit.ZIB, Unit.YIB]
    else:
        units = [Unit.B, Unit.KB, Unit.MB, Unit.GB, Unit.TB, 
                 Unit.PB, Unit.EB, Unit.ZB, Unit.YB]
    
    # Добавляем шуточные единицы, если значение очень большое
    jpy_bytes = Decimal(str(TO_BYTES[Unit.JPY]))
    gpy_bytes = Decimal(str(TO_BYTES[Unit.GPY]))
    hpy_bytes = Decimal(str(TO_BYTES[Unit.HPY]))
    ipy_bytes = Decimal(str(TO_BYTES[Unit.IPY]))
    
    if bytes_dec > jpy_bytes:
        units.extend([Unit.IPY, Unit.HPY, Unit.GPY, Unit.JPY])
    elif bytes_dec > gpy_bytes:
        units.extend([Unit.IPY, Unit.HPY, Unit.GPY])
    elif bytes_dec > hpy_bytes:
        units.extend([Unit.IPY, Unit.HPY])
    elif bytes_dec > ipy_bytes:
        units.extend([Unit.IPY])
    
    # Ограничиваем максимальной единицей, если указана
    if max_unit and max_unit in units:
        units = [u for u in units if TO_BYTES[u] <= TO_BYTES[max_unit]]
    
    # Идём с конца (самые большие единицы) и ищем подходящую
    for unit in reversed(units):
        converted = Converter.from_bytes(bytes_dec, unit)
        if float(converted) >= min_value:
            return unit
    
    return Unit.B


def best_format(
    bytes_val: Union[int, float, Decimal],
    binary: bool = False,
    precision: int = 2
) -> str:
    """
    Форматирует байты, автоматически выбирая оптимальную единицу
    
    Это удобная обёртка над format_size() + best_unit()
    
    Args:
        bytes_val: Количество байт
        binary: Использовать двоичные единицы
        precision: Количество знаков после запятой
    
    Returns:
        Отформатированная строка
        
    Примеры:
        >>> best_format(1234567890)
        '1.23 GB'
        
        >>> best_format(1234567890, binary=True)
        '1.15 GiB'
        
        >>> best_format(1500)
        '1.50 KB'
        
        >>> best_format(1500, binary=True)
        '1.46 KiB'
    """
    
    unit = best_unit(bytes_val, binary)
    return format_size(bytes_val, unit=Unit.B, target_unit=unit, precision=precision)
