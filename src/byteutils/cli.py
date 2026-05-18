"""CLI-интерфейс для работы с библиотекой из командной строки"""

import argparse
import sys

from .units import Unit, UNIT_NAMES
from .converter import Converter
from .formatter import format_size
from .parser import parse_size


def main():
    """Главная точка входа для CLI"""
    
    parser = argparse.ArgumentParser(
        prog="byteutils",
        description="Конвертер единиц памяти - работа с байтами, килобайтами, мегабайтами и другими единицами",
        epilog="Примеры:\n  byteutils convert 1 GB MB\n  byteutils format 1234567890\n  byteutils parse '2.5 MB'"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")
    
    # ===== Команда: convert (конвертация) =====
    convert_parser = subparsers.add_parser("convert", help="Конвертировать между единицами")
    convert_parser.add_argument("value", type=float, help="Числовое значение")
    convert_parser.add_argument("from_unit", type=str, help="Исходная единица (GB, MB, KiB и т.д.)")
    convert_parser.add_argument("to_unit", type=str, help="Целевая единица")
    
    # ===== Команда: format (форматирование) =====
    format_parser = subparsers.add_parser("format", help="Форматировать размер в человекочитаемый вид")
    format_parser.add_argument("value", type=float, help="Числовое значение")
    format_parser.add_argument("--unit", type=str, default=None, help="Исходная единица (по умолчанию байты)")
    format_parser.add_argument("--target", type=str, default=None, help="Целевая единица (авто-выбор по умолчанию)")
    format_parser.add_argument("--binary", action="store_true", help="Использовать двоичные единицы (KiB, MiB...)")
    format_parser.add_argument("--precision", type=int, default=2, help="Точность (знаков после запятой), по умолчанию 2")
    format_parser.add_argument("--full-name", action="store_true", help="Использовать полные названия (килобайт вместо KB)")
    
    # ===== Команда: parse (парсинг) =====
    parse_parser = subparsers.add_parser("parse", help="Распарсить строку с размером")
    parse_parser.add_argument("string", type=str, help="Строка вида '1.5 GB' или '2 KiB'")
    parse_parser.add_argument("--bytes", action="store_true", help="Показать результат в байтах")
    
    # ===== Команда: list (список единиц) =====
    list_parser = subparsers.add_parser("list", help="Список всех доступных единиц измерения")
    
    # ===== Команда: version (версия) =====
    version_parser = subparsers.add_parser("version", help="Показать версию библиотеки")
    
    args = parser.parse_args()
    
    # ===== Обработка команды convert =====
    if args.command == "convert":
        try:
            from_unit = Unit(args.from_unit.upper())
            to_unit = Unit(args.to_unit.upper())
            result = Converter.convert_float(args.value, from_unit, to_unit)
            print(f"{args.value} {from_unit.value} = {result} {to_unit.value}")
        except ValueError:
            print(f"Ошибка: неизвестная единица измерения.")
            print("Доступные: B, KB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB, IPY, HPY, GPY, JPY")
            sys.exit(1)
    
    # ===== Обработка команды format =====
    elif args.command == "format":
        try:
            unit = Unit(args.unit.upper()) if args.unit else None
            target = Unit(args.target.upper()) if args.target else None
            result = format_size(
                args.value, 
                unit=unit, 
                target_unit=target,
                binary=args.binary, 
                precision=args.precision,
                use_full_name=args.full_name
            )
            print(result)
        except ValueError as e:
            print(f"Ошибка: {e}")
            sys.exit(1)
    
    # ===== Обработка команды parse =====
    elif args.command == "parse":
        try:
            if args.bytes:
                result = parse_size(args.string)
                print(f"{result} байт")
            else:
                val, unit = parse_size(args.string, return_unit=True)
                # Убираем лишние нули в конце
                if val == val.to_integral():
                    print(f"{int(val)} {unit.value}")
                else:
                    print(f"{val} {unit.value}")
        except ValueError as e:
            print(f"Ошибка: {e}")
            sys.exit(1)
    
    # ===== Обработка команды list =====
    elif args.command == "list":
        print("\n📊 Доступные единицы измерения:")
        print("=" * 40)
        print(f"{'Единица':<8} {'Тип':<12} {'Название'}")
        print("=" * 40)
        
        for unit in Unit:
            # Определяем тип единицы
            if unit in [Unit.B, Unit.KB, Unit.MB, Unit.GB, Unit.TB, Unit.PB, Unit.EB, Unit.ZB, Unit.YB]:
                unit_type = "десятичная"
            elif unit in [Unit.KIB, Unit.MIB, Unit.GIB, Unit.TIB, Unit.PIB, Unit.EIB, Unit.ZIB, Unit.YIB]:
                unit_type = "двоичная"
            else:
                unit_type = "шуточная"
            
            name = UNIT_NAMES.get(unit, "")
            print(f"{unit.value:<8} {unit_type:<12} {name}")
        
        print("=" * 40)
        print(f"\nВсего единиц: {len(Unit)}")
    
    # ===== Обработка команды version =====
    elif args.command == "version":
        from . import __version__
        print(f"byteutils {__version__}")


if __name__ == "__main__":
    main()
