"""Конвертация между любыми единицами измерения"""

from decimal import Decimal, getcontext
from typing import Union

from .units import Unit, TO_BYTES

# Устанавливаем высокую точность для работы с очень большими числами
getcontext().prec = 50


class Converter:
    """
    Конвертер объёмов памяти
    
    Позволяет конвертировать между любыми единицами измерения:
    - байты, килобайты, мегабайты, гигабайты и т.д.
    - кибибайты, мебибайты, гибибайты и т.д.
    - шуточные единицы IPY, HPY, GPY, JPY
    
    Примеры:
        >>> Converter.convert(1, Unit.GB, Unit.MB)
        Decimal('1000')
        
        >>> Converter.convert(1, Unit.GIB, Unit.MIB)
        Decimal('1024')
        
        >>> Converter.to_bytes(1, Unit.KB)
        Decimal('1000')
        
        >>> Converter.from_bytes(1048576, Unit.MIB)
        Decimal('1')
    """
    
    @staticmethod
    def to_bytes(value: Union[int, float, Decimal], unit: Unit) -> Decimal:
        """
        Переводит значение в байты
        
        Args:
            value: Числовое значение в исходной единице
            unit: Исходная единица измерения
            
        Returns:
            Количество байт (Decimal для высокой точности)
            
        Пример:
            >>> Converter.to_bytes(1, Unit.KB)
            Decimal('1000')
            >>> Converter.to_bytes(1, Unit.MIB)
            Decimal('1048576')
        """
        value_dec = Decimal(str(value))
        factor = Decimal(str(TO_BYTES[unit]))
        return value_dec * factor
    
    @staticmethod
    def from_bytes(bytes_val: Union[int, float, Decimal], unit: Unit) -> Decimal:
        """
        Переводит байты в указанную единицу измерения
        
        Args:
            bytes_val: Количество байт
            unit: Целевая единица измерения
            
        Returns:
            Значение в целевой единице
            
        Пример:
            >>> Converter.from_bytes(1000, Unit.KB)
            Decimal('1')
            >>> Converter.from_bytes(1048576, Unit.MIB)
            Decimal('1')
        """
        bytes_dec = Decimal(str(bytes_val))
        factor = Decimal(str(TO_BYTES[unit]))
        return bytes_dec / factor
    
    @staticmethod
    def convert(value: Union[int, float, Decimal], 
                from_unit: Unit, 
                to_unit: Unit) -> Decimal:
        """
        Конвертирует значение из одной единицы в другую
        
        Args:
            value: Значение в исходной единице
            from_unit: Исходная единица измерения
            to_unit: Целевая единица измерения
            
        Returns:
            Значение в целевой единице
            
        Пример:
            >>> Converter.convert(1, Unit.GB, Unit.MB)
            Decimal('1000')
            >>> Converter.convert(1, Unit.TB, Unit.GB)
            Decimal('1000')
            >>> Converter.convert(1024, Unit.KIB, Unit.MIB)
            Decimal('1')
        """
        bytes_val = Converter.to_bytes(value, from_unit)
        return Converter.from_bytes(bytes_val, to_unit)
    
    @staticmethod
    def convert_float(value: float, from_unit: Unit, to_unit: Unit) -> float:
        """
        Конвертирует значение из одной единицы в другую с возвратом float
        
        ВНИМАНИЕ: Может терять точность для очень больших чисел!
        Для максимальной точности используйте convert()
        
        Args:
            value: Значение в исходной единице
            from_unit: Исходная единица измерения
            to_unit: Целевая единица измерения
            
        Returns:
            Значение в целевой единице (float)
            
        Пример:
            >>> Converter.convert_float(1, Unit.GB, Unit.MB)
            1000.0
        """
        return float(Converter.convert(value, from_unit, to_unit))
