"""Точка входа CLI-приложения визуализации графа зависимостей."""

import sys
from cli import parse_config
from parser import download_apkindex, extract_apkindex_text, get_direct_deps


def print_direct_deps(package: str, version: str, deps: list[str]) -> None:
    """Выводит прямые зависимости пакета на экран."""
    print(f"Прямые зависимости пакета {package} ({version}):")
    if not deps:
        print("  (зависимости отсутствуют)")
        return
    for dep in deps:
        print(f"  - {dep}")


def main() -> int:
    """Основная функция запуска приложения."""
    try:
        config = parse_config()
    except ValueError as err:
        print(f"Ошибка конфигурации: {err}", file=sys.stderr)
        return 1

    if config["test_mode"]:
        print("Режим тестирования будет добавлен на Этапе 3.")
        return 0

    try:
        archive = download_apkindex(str(config["repo"]))
        index_text = extract_apkindex_text(archive)
        deps = get_direct_deps(
            index_text, str(config["package"]), str(config["version"])
        )
        print_direct_deps(
            str(config["package"]), str(config["version"]), deps
        )
    except Exception as err:
        print(f"Ошибка получения данных: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
