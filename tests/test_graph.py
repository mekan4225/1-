"""Модульные тесты построения графа зависимостей (Этап 3)."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)
from graph import build_dependency_graph
from parser import parse_test_repo


class TestDependencyGraph(unittest.TestCase):
    """Тесты алгоритма BFS без рекурсии и обработки циклов."""

    def test_transitive_and_cyclic_graph(self) -> None:
        """Проверяет построение графа с транзитивностью и циклом."""
        repo = {
            "A": ["B", "D"],
            "B": ["C", "E"],
            "C": ["B"],
            "D": ["E"],
            "E": [],
        }
        graph = build_dependency_graph("A", repo)
        self.assertEqual(set(graph.keys()), {"A", "B", "C", "D", "E"})
        self.assertEqual(graph["C"], ["B"])

    def test_parse_sample_repo_file(self) -> None:
        """Проверяет чтение файла тестового репозитория."""
        sample_path = os.path.join(
            os.path.dirname(__file__), "sample_repo.txt"
        )
        repo = parse_test_repo(sample_path)
        self.assertIn("A", repo)
        self.assertEqual(repo["A"], ["B", "D"])


if __name__ == "__main__":
    unittest.main()
