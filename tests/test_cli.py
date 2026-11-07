"""Модульные тесты для проверки конфигурации Этапа 1."""

import os
import sys
import tempfile
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)
from cli import parse_config


class TestCliConfig(unittest.TestCase):
    """Тесты разбора и валидации параметров CLI."""

    def test_valid_url_config(self) -> None:
        """Проверяет корректный разбор параметров с URL."""
        args = [
            "--package", "curl",
            "--repo", "https://alpinelinux.org",
            "--version", "8.9.1-r0",
            "--output", "out.svg",
        ]
        cfg = parse_config(args)
        self.assertEqual(cfg["package"], "curl")
        self.assertFalse(cfg["test_mode"])

    def test_valid_test_mode_config(self) -> None:
        """Проверяет корректный режим тестового репозитория."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            args = [
                "--package", "A",
                "--repo", tmp_path,
                "--test-mode",
                "--version", "1.0",
            ]
            cfg = parse_config(args)
            self.assertTrue(cfg["test_mode"])
        finally:
            os.remove(tmp_path)

    def test_invalid_url_raises(self) -> None:
        """Проверяет ошибку при невалидном URL."""
        args = [
            "--package", "curl",
            "--repo", "not_a_url",
            "--version", "1.0",
        ]
        with self.assertRaises(ValueError):
            parse_config(args)

    def test_invalid_output_extension(self) -> None:
        """Проверяет ошибку при неверном расширении файла."""
        args = [
            "--package", "curl",
            "--repo", "https://example.com",
            "--version", "1.0",
            "--output", "graph.png",
        ]
        with self.assertRaises(ValueError):
            parse_config(args)


if __name__ == "__main__":
    unittest.main()
