"""Форматирование объёмов памяти в человекочитаемый вид"""

from typing import Optional, Union
from decimal import Decimal

from .units import Unit, TO_BYTES, UNIT_NAMES
from .converter import Converter


def format_size(
    value: Union[int, float, Decimal],
    unit: Optional[Unit] = None,
    target_unit: Optional[Unit] = None,
    precision: int = 2,
    binary: bool = False,
    use_suffix: bool = True,
    use_full_name: bool = False,
    thousands_sep: bool = False,
    strip_trailing_zeros: bool = False
) -> str:
    """
    Форматирует объём памяти в человекочитаемый вид
    
    Args:
        value: Числовое значение
        unit: Исходная единица (если None, считается что value в байтах)
        target_unit: Целевая единица (если None, выбирается автоматически)
        precision: Количество знаков после запятой (по умолчанию 2)
        binary: Использовать двоичные единицы (KiB, MiB...)
        use_suffix: Добавлять суффикс единицы измерения
        use_full_name: Использовать полное название ("килобайт" вместо "KB")
        thousands_sep: Разделять тысячи запятыми/пробелами
        strip_trailing_zeros: Убирать незначащие нули
    
    Returns:
        Отформатированная строка
        
    Примеры:
        >>> format_size(1234567890)
        '1.23 GB'
        
        >>> format_size(1024, binary=True)
        '1.00 KiB'
        
        >>> format_size(1500000, target_unit=Unit.KB)
        '1500.00 KB'
        
        >>> format_size(1024, use_full_name=True)
        '1.02 килобайта'
        
        >>> format_size(1234567, thousands_sep=True)
        '1 234 567.00 B'
    """
    
    # Если единица не указана, считаем что значение в байтах
    if unit is None:
        unit = Unit.B
    
    # Переводим в байты
    bytes_val = Converter.to_bytes(value, unit)
    
    # Если целевая единица не указана, выбираем автоматически
    if target_unit is None:
        target_unit = _auto_select_unit(bytes_val, binary)
    
    # Конвертируем в целевую единицу
    converted = Converter.from_bytes(bytes_val, target_unit)
    
    # Форматируем число
    number_str = _format_number(
        converted, 
        precision=precision,
        strip_trailing_zeros=strip_trailing_zeros,
        thousands_sep=thousands_sep
    )
    
    # Добавляем суффикс если нужно
    if use_suffix:
        if use_full_name:
            suffix = UNIT_NAMES[target_unit]
            # Склоняем в зависимости от числа
            if float(converted) != 1:
                if suffix.endswith("т"):
                    suffix += "а"      # байт -> байта
                elif suffix.endswith("й"):
                    suffix = suffix[:-1] + "я"  # килобайт -> килобайта
                else:
                    suffix += "ов"     # мегабайт -> мегабайтов
        else:
            suffix = target_unit.value
        
        return f"{number_str} {suffix}"
    
    return number_str


def _auto_select_unit(bytes_val: Decimal, binary: bool = False) -> Unit:
    """
    Автоматически выбирает оптимальную единицу для заданного количества байт
    
    Args:
        bytes_val: Количество байт
        binary: Использовать двоичные единицы
        
    Returns:
        Оптимальная единица измерения
    """
    
    if binary:
        units = [Unit.B, Unit.KIB, Unit.MIB, Unit.GIB, Unit.TIB, 
                 Unit.PIB, Unit.EIB, Unit.ZIB, Unit.YIB]
    else:
        units = [Unit.B, Unit.KB, Unit.MB, Unit.GB, Unit.TB, 
                 Unit.PB, Unit.EB, Unit.ZB, Unit.YB]
    
    # Идём с конца (самые большие единицы)
    for unit in reversed(units):
        if bytes_val >= Decimal(str(TO_BYTES[unit])):
            return unit
    
    return Unit.B


def _format_number(value: Decimal, precision: int = 2, 
                   strip_trailing_zeros: bool = False,
                   thousands_sep: bool = False) -> str:
    """
    Форматирует число с заданными параметрами
    
    Args:
        value: Число для форматирования
        precision: Количество знаков после запятой
        strip_trailing_zeros: Убрать незначащие нули
        thousands_sep: Добавить разделители тысяч
        
    Returns:
        Отформатированная строка
    """
    
    # Округляем до нужной точности
    rounded = round(value, precision)
    
    # Преобразуем в строку
    if strip_trailing_zeros:
        # Убираем .0 и лишние нули в конце
        s = f"{rounded:f}".rstrip('0').rstrip('.')
    else:
        s = f"{rounded:.{precision}f}"
    
    # Добавляем разделители тысяч
    if thousands_sep and '.' in s:
        int_part, frac_part = s.split('.')
        # Используем пробел как разделитель тысяч (можно заменить на ',' или ' ')
        int_part = f"{int(int_part):,}".replace(',', ' ')
        s = f"{int_part}.{frac_part}"
    elif thousands_sep and '.' not in s:
        s = f"{int(int_part):,}".replace(',', ' ')
    
    return s
