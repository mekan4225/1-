"""Модульные тесты построения графа и порядка загрузки (Этапы 3-4)."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)
from graph import build_dependency_graph, get_load_order
from parser import parse_test_repo


class TestDependencyGraph(unittest.TestCase):
    """Тесты алгоритма BFS, циклов и порядка загрузки."""

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

    def test_load_order_dependencies_first(self) -> None:
        """Проверяет, что зависимости идут раньше корневого пакета."""
        repo = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        graph = build_dependency_graph("A", repo)
        order = get_load_order("A", graph)
        self.assertEqual(order[-1], "A")
        self.assertEqual(order[0], "D")

    def test_load_order_with_cycle(self) -> None:
        """Проверяет корректность порядка загрузки при наличии цикла."""
        repo = {"A": ["B"], "B": ["C"], "C": ["B"]}
        graph = build_dependency_graph("A", repo)
        order = get_load_order("A", graph)
        self.assertEqual(order[-1], "A")
        self.assertEqual(len(order), 3)

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
