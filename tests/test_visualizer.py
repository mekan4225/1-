"""Модульные тесты генерации PlantUML (Этап 5)."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)
from visualizer import build_plantuml, encode_plantuml_text


class TestVisualizer(unittest.TestCase):
    """Тесты формирования текста PlantUML и кодирования URL."""

    def test_build_plantuml_structure(self) -> None:
        """Проверяет наличие тегов PlantUML и связей между пакетами."""
        graph = {"A": ["B", "C"], "B": [], "C": []}
        puml = build_plantuml("A", graph)
        self.assertTrue(puml.startswith("@startuml"))
        self.assertTrue(puml.endswith("@enduml"))
        self.assertIn("A --> B", puml)
        self.assertIn("A --> C", puml)

    def test_encode_plantuml_non_empty(self) -> None:
        """Проверяет кодирование PlantUML-строки для запроса SVG."""
        encoded = encode_plantuml_text("@startuml\nA --> B\n@enduml")
        self.assertTrue(len(encoded) > 0)


if __name__ == "__main__":
    unittest.main()
