"""Точка входа CLI-приложения визуализации графа зависимостей."""

import sys
from cli import parse_config
from graph import build_dependency_graph
from parser import (
    download_apkindex,
    extract_apkindex_text,
    get_direct_deps,
    parse_all_packages,
    parse_test_repo,
)


def print_graph(graph: dict[str, list[str]]) -> None:
    """Выводит построенный граф зависимостей на экран."""
    print("Граф зависимостей (BFS):")
    for pkg, deps in graph.items():
        deps_str = ", ".join(deps) if deps else "(нет)"
        print(f"  {pkg} -> {deps_str}")


def resolve_graph(config: dict[str, str | bool]) -> dict[str, list[str]]:
    """Загружает данные и строит граф зависимостей по конфигурации."""
    pkg = str(config["package"])
    repo = str(config["repo"])
    if config["test_mode"]:
        repo_map = parse_test_repo(repo)
        if pkg not in repo_map:
            raise ValueError(f"Пакет {pkg} не найден в тестовом файле.")
        return build_dependency_graph(pkg, repo_map)

    archive = download_apkindex(repo)
    index_text = extract_apkindex_text(archive)
    direct = get_direct_deps(index_text, pkg, str(config["version"]))
    repo_map = parse_all_packages(index_text)
    return build_dependency_graph(pkg, repo_map, direct)


def main() -> int:
    """Основная функция запуска приложения."""
    try:
        config = parse_config()
        graph = resolve_graph(config)
        print_graph(graph)
    except Exception as err:
        print(f"Ошибка выполнения: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
