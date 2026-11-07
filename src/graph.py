"""Модуль построения графа зависимостей с использованием BFS без рекурсии."""

from collections import deque


def build_dependency_graph(
    root_pkg: str,
    repo_map: dict[str, list[str]],
    root_deps: list[str] | None = None,
) -> dict[str, list[str]]:
    """Строит граф зависимостей алгоритмом BFS без рекурсии."""
    graph: dict[str, list[str]] = {}
    visited: set[str] = {root_pkg}
    queue: deque[str] = deque([root_pkg])

    while queue:
        current = queue.popleft()
        if current == root_pkg and root_deps is not None:
            deps = root_deps
        else:
            deps = repo_map.get(current, [])
        graph[current] = list(deps)

        for dep in deps:
            if dep not in visited:
                visited.add(dep)
                queue.append(dep)

    return graph
