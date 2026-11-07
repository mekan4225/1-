"""Модульные тесты для парсера APKINDEX (Этап 2)."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)
from parser import get_direct_deps, parse_dependencies

SAMPLE_INDEX = """P:zlib
V:1.2.13-r1
D:so:libc.musl-x86_64.so.1

P:curl
V:8.9.1-r0
D:ca-certificates-bundle libcurl>=8.9.1 so:libc.musl-x86_64.so.1
"""


class TestApkParser(unittest.TestCase):
    """Тесты извлечения прямых зависимостей."""

    def test_parse_dependencies_cleans_prefixes(self) -> None:
        """Проверяет очистку префиксов so: и операторов версий."""
        raw = "ca-certificates-bundle libcurl>=8.9.1 so:libc.musl-x86_64.so.1"
        deps = parse_dependencies(raw)
        self.assertEqual(
            deps,
            ["ca-certificates-bundle", "libcurl", "libc.musl-x86_64.so.1"],
        )

    def test_get_direct_deps_success(self) -> None:
        """Проверяет поиск зависимостей для точной версии пакета."""
        deps = get_direct_deps(SAMPLE_INDEX, "curl", "8.9.1-r0")
        self.assertIn("libcurl", deps)

    def test_get_direct_deps_not_found(self) -> None:
        """Проверяет ошибку при отсутствии пакета или версии."""
        with self.assertRaises(ValueError):
            get_direct_deps(SAMPLE_INDEX, "curl", "9.9.9-r0")


if __name__ == "__main__":
    unittest.main()
