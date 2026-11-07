"""Модуль загрузки и парсинга индекса пакетов Alpine Linux (APKINDEX)."""

import io
import tarfile
import urllib.request

DEFAULT_TIMEOUT = 15
INDEX_SUFFIX = "/v3.18/main/x86_64/APKINDEX.tar.gz"
VERSION_OPERATORS = ("<=", ">=", "=", "<", ">")


def download_apkindex(repo_url: str) -> bytes:
    """Скачивает архив APKINDEX.tar.gz из репозитория в память."""
    url = repo_url.rstrip("/") + INDEX_SUFFIX
    try:
        with urllib.request.urlopen(url, timeout=DEFAULT_TIMEOUT) as resp:
            return resp.read()
    except Exception as err:
        raise RuntimeError(f"Ошибка загрузки {url}: {err}") from err


def extract_apkindex_text(archive_bytes: bytes) -> str:
    """Распаковывает APKINDEX.tar.gz и извлекает текст файла APKINDEX."""
    file_obj = io.BytesIO(archive_bytes)
    with tarfile.open(fileobj=file_obj, mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.name == "APKINDEX":
                extracted = tar.extractfile(member)
                if extracted is not None:
                    return extracted.read().decode("utf-8", errors="ignore")
    raise RuntimeError("Файл APKINDEX не найден внутри архива.")


def clean_dependency_name(raw_dep: str) -> str:
    """Очищает имя зависимости от префиксов и операторов версий."""
    dep = raw_dep.split(":", 1)[-1] if ":" in raw_dep else raw_dep
    for operator in VERSION_OPERATORS:
        if operator in dep:
            dep = dep.split(operator, 1)[0]
            break
    return dep.strip()


def parse_dependencies(deps_line: str) -> list[str]:
    """Разбирает строку зависимостей D: в список уникальных имен."""
    result: list[str] = []
    for raw_dep in deps_line.split():
        cleaned = clean_dependency_name(raw_dep)
        if cleaned and cleaned not in result:
            result.append(cleaned)
    return result


def get_direct_deps(
    index_text: str, target_pkg: str, target_ver: str
) -> list[str]:
    """Ищет пакет нужной версии в индексе и возвращает его зависимости."""
    pkg, ver, deps = "", "", ""
    for raw_line in index_text.splitlines():
        line = raw_line.strip()
        if not line:
            if pkg == target_pkg and ver == target_ver:
                return parse_dependencies(deps)
            pkg, ver, deps = "", "", ""
        elif line.startswith("P:"):
            pkg = line[2:]
        elif line.startswith("V:"):
            ver = line[2:]
        elif line.startswith("D:"):
            deps = line[2:]
    if pkg == target_pkg and ver == target_ver:
        return parse_dependencies(deps)
    raise ValueError(f"Пакет {target_pkg} версии {target_ver} не найден.")
