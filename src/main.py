"""Точка входа CLI-приложения визуализации графа зависимостей."""

import sys
from cli import parse_config


def print_config(config: dict[str, str | bool]) -> None:
    """Выводит параметры конфигурации в формате ключ: значение."""
    for key, value in config.items():
        print(f"{key}: {value}")


def main() -> int:
    """Основная функция запуска приложения."""
    try:
        config = parse_config()
    except ValueError as err:
        print(f"Ошибка конфигурации: {err}", file=sys.stderr)
        return 1

    print_config(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
