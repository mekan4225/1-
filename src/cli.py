"""Модуль разбора и валидации аргументов командной строки."""

import argparse
import os
from urllib.parse import urlparse


def validate_non_empty(value: str, field_name: str) -> str:
    """Проверяет, что строковый параметр не является пустым."""
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"Параметр '{field_name}' не может быть пустым.")
    return cleaned


def validate_repo(repo: str, test_mode: bool) -> str:
    """Проверяет корректность URL репозитория или пути к файлу."""
    cleaned = validate_non_empty(repo, "repo")
    if test_mode:
        if not os.path.isfile(cleaned):
            raise ValueError(f"Тестовый файл не найден: {cleaned}")
        return cleaned
    parsed = urlparse(cleaned)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Некорректный URL репозитория: {cleaned}")
    return cleaned


def validate_output(output: str) -> str:
    """Проверяет имя выходного SVG-файла."""
    cleaned = validate_non_empty(output, "output")
    if not cleaned.lower().endswith(".svg"):
        raise ValueError("Выходной файл должен иметь расширение .svg")
    return cleaned


def build_parser() -> argparse.ArgumentParser:
    """Создает и настраивает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализатор графа зависимостей пакетов apk."
    )
    parser.add_argument(
        "--package", required=True, help="Имя анализируемого пакета."
    )
    parser.add_argument(
        "--repo", required=True, help="URL репозитория или путь к файлу."
    )
    parser.add_argument(
        "--test-mode", action="store_true", help="Режим тестового репозитория."
    )
    parser.add_argument(
        "--version", required=True, help="Версия анализируемого пакета."
    )
    parser.add_argument(
        "--output", default="graph.svg", help="Имя выходного SVG-файла."
    )
    parser.add_argument(
        "--load-order",
        action="store_true",
        help="Вывести порядок загрузки зависимостей.",
    )
    return parser


def parse_config(argv: list[str] | None = None) -> dict[str, str | bool]:
    """Разбирает и валидирует параметры запуска приложения."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return {
        "package": validate_non_empty(args.package, "package"),
        "repo": validate_repo(args.repo, args.test_mode),
        "test_mode": bool(args.test_mode),
        "version": validate_non_empty(args.version, "version"),
        "output": validate_output(args.output),
        "load_order": bool(args.load_order),
    }
