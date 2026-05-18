"""CLI-интерфейс для работы из командной строки"""

import argparse
import sys

from .units import Unit, UNIT_NAMES
from .converter import Converter
from .formatter import format_size
from .parser import parse_size


def _normalize_unit_name(unit_str: str) -> str:
    """Нормализует название единицы (приводит к формату Unit)"""
    unit_upper = unit_str.upper()
    
    # Соответствие между разными вариантами написания
    mapping = {
        "B": "B",
        "KB": "KB", "KIB": "KIB",
        "MB": "MB", "MIB": "MIB",
        "GB": "GB", "GIB": "GIB",
        "TB": "TB", "TIB": "TIB",
        "PB": "PB", "PIB": "PIB",
        "EB": "EB", "EIB": "EIB",
        "ZB": "ZB", "ZIB": "ZIB",
        "YB": "YB", "YIB": "YIB",
        "IPY": "IPY", "HPY": "HPY", "GPY": "GPY", "JPY": "JPY",
    }
    
    # Если ввели KiB, MiB, GiB и т.д. (с маленькой i)
    if unit_upper == "KIB":
        return "KIB"
    if unit_upper == "MIB":
        return "MIB"
    if unit_upper == "GIB":
        return "GIB"
    if unit_upper == "TIB":
        return "TIB"
    if unit_upper == "PIB":
        return "PIB"
    if unit_upper == "EIB":
        return "EIB"
    if unit_upper == "ZIB":
        return "ZIB"
    if unit_upper == "YIB":
        return "YIB"
    
    # Если ввели KB, MB, GB и т.д.
    if unit_upper in mapping:
        return mapping[unit_upper]
    
    return unit_upper


def main():
    """Главная точка входа для CLI"""
    
    parser = argparse.ArgumentParser(
        prog="gpybyte",
        description="gpybyte - конвертер единиц памяти (поддержка стандарта JPYByte: IPY/HPY/GPY/JPY)",
        epilog="Примеры:\n  gpybyte convert 1 GB MB\n  gpybyte convert 1 GiB MiB\n  gpybyte format 1234567890\n  gpybyte parse '2.5 MB'\n  gpybyte convert 1 GPY JPY"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")
    
    # ===== Команда: convert =====
    convert_parser = subparsers.add_parser("convert", help="Конвертировать между единицами")
    convert_parser.add_argument("value", type=float, help="Числовое значение")
    convert_parser.add_argument("from_unit", type=str, help="Исходная единица (GB, MB, KiB, GiB, IPY, GPY и т.д.)")
    convert_parser.add_argument("to_unit", type=str, help="Целевая единица")
    
    # ===== Команда: format =====
    format_parser = subparsers.add_parser("format", help="Форматировать размер в человекочитаемый вид")
    format_parser.add_argument("value", type=float, help="Числовое значение")
    format_parser.add_argument("--unit", type=str, default=None, help="Исходная единица (по умолчанию байты)")
    format_parser.add_argument("--target", type=str, default=None, help="Целевая единица (авто-выбор по умолчанию)")
    format_parser.add_argument("--binary", action="store_true", help="Использовать двоичные единицы (KiB, MiB...)")
    format_parser.add_argument("--precision", type=int, default=2, help="Точность (знаков после запятой), по умолчанию 2")
    format_parser.add_argument("--full-name", action="store_true", help="Использовать полные названия (килобайт вместо KB)")
    
    # ===== Команда: parse =====
    parse_parser = subparsers.add_parser("parse", help="Распарсить строку с размером")
    parse_parser.add_argument("string", type=str, help="Строка вида '1.5 GB' или '2 KiB' или '10 GPY'")
    parse_parser.add_argument("--bytes", action="store_true", help="Показать результат в байтах")
    
    # ===== Команда: list =====
    list_parser = subparsers.add_parser("list", help="Список всех доступных единиц измерения")
    
    # ===== Команда: version =====
    version_parser = subparsers.add_parser("version", help="Показать версию библиотеки")
    
    args = parser.parse_args()
    
    # ===== Обработка команды convert =====
    if args.command == "convert":
        try:
            from_unit_name = _normalize_unit_name(args.from_unit)
            to_unit_name = _normalize_unit_name(args.to_unit)
            
            from_unit = Unit[from_unit_name]
            to_unit = Unit[to_unit_name]
            
            result = Converter.convert_float(args.value, from_unit, to_unit)
            print(f"{args.value} {from_unit.value} = {result} {to_unit.value}")
        except KeyError as e:
            print(f"Ошибка: неизвестная единица измерения '{args.from_unit}' или '{args.to_unit}'")
            print("Доступные: B, KB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB, IPY, HPY, GPY, JPY")
            print("Также поддерживаются: KIB, MIB, GIB, TIB, PIB, EIB, ZIB, YIB")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка: {e}")
            sys.exit(1)
    
    # ===== Обработка команды format =====
    elif args.command == "format":
        try:
            unit = None
            if args.unit:
                unit_name = _normalize_unit_name(args.unit)
                unit = Unit[unit_name]
            
            target = None
            if args.target:
                target_name = _normalize_unit_name(args.target)
                target = Unit[target_name]
            
            result = format_size(
                args.value, 
                unit=unit, 
                target_unit=target,
                binary=args.binary, 
                precision=args.precision,
                use_full_name=args.full_name
            )
            print(result)
        except KeyError as e:
            print(f"Ошибка: неизвестная единица измерения")
            sys.exit(1)
        except Exception as e:
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
                if val == val.to_integral():
                    print(f"{int(val)} {unit.value}")
                else:
                    print(f"{val} {unit.value}")
        except ValueError as e:
            print(f"Ошибка: {e}")
            sys.exit(1)
    
    # ===== Обработка команды list =====
    elif args.command == "list":
        print("\n📊 Доступные единицы измерения (стандарт JPYByte):")
        print("=" * 50)
        print(f"{'Единица':<10} {'Тип':<18} {'Название'}")
        print("=" * 50)
        
        for unit in Unit:
            if unit in [Unit.B, Unit.KB, Unit.MB, Unit.GB, Unit.TB, Unit.PB, Unit.EB, Unit.ZB, Unit.YB]:
                unit_type = "десятичная"
            elif unit in [Unit.KIB, Unit.MIB, Unit.GIB, Unit.TIB, Unit.PIB, Unit.EIB, Unit.ZIB, Unit.YIB]:
                unit_type = "двоичная"
            elif unit in [Unit.IPY, Unit.HPY, Unit.GPY, Unit.JPY]:
                unit_type = "стандарт JPYByte"
            else:
                unit_type = "другая"
            
            name = UNIT_NAMES.get(unit, "")
            print(f"{unit.value:<10} {unit_type:<18} {name}")
        
        print("=" * 50)
        print(f"\nВсего единиц: {len(Unit)}")
        print("\n📐 Стандарт JPYByte для ГИС:")
        print("  IPY (айпибайт) = 2^90 байт")
        print("  HPY (эйчпибайт) = 1000 IPY")
        print("  GPY (джипибайт) = 1000 HPY")
        print("  JPY (джейпибайт) = 1000 GPY")
    
    # ===== Обработка команды version =====
    elif args.command == "version":
        from . import __version__
        print(f"gpybyte {__version__} - поддержка стандарта JPYByte")


if __name__ == "__main__":
    main()
