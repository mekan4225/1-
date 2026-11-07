"""Модуль генерации описания PlantUML и сохранения графа в формате SVG."""

import string
import urllib.request
import zlib

PLANTUML_SVG_URL = "https://plantuml.com"
REQUEST_TIMEOUT = 15
B64_STANDARD = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
)
B64_PLANTUML = (
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
)


def encode_plantuml_text(puml_text: str) -> str:
    """Сжимает текст PlantUML алгоритмом Deflate и кодирует для URL."""
    compressed = zlib.compress(puml_text.encode("utf-8"))[2:-4]
    encoded = _encode_bytes_plantuml(compressed)
    return encoded


def _encode_bytes_plantuml(data: bytes) -> str:
    """Кодирует байты в специальный 64-символьный алфавит PlantUML."""
    res: list[str] = []
    for idx in range(0, len(data), 3):
        b1 = data[idx]
        b2 = data[idx + 1] if idx + 1 < len(data) else 0
        b3 = data[idx + 2] if idx + 2 < len(data) else 0
        res.append(B64_PLANTUML[b1 >> 2])
        res.append(B64_PLANTUML[((b1 & 0x3) << 4) | (b2 >> 4)])
        res.append(B64_PLANTUML[((b2 & 0xF) << 2) | (b3 >> 6)])
        res.append(B64_PLANTUML[b3 & 0x3F])
    return "".join(res)


def _safe_alias(name: str) -> str:
    """Преобразует имя пакета в безопасный идентификатор PlantUML."""
    allowed = set(string.ascii_letters + string.digits + "_")
    return "".join(ch if ch in allowed else "_" for ch in name)


def build_plantuml(root_pkg: str, graph: dict[str, list[str]]) -> str:
    """Формирует текстовое представление графа на языке PlantUML."""
    lines: list[str] = ["@startuml", "skinparam monochrome true"]
    for pkg in graph:
        alias = _safe_alias(pkg)
        label = f"{pkg} (root)" if pkg == root_pkg else pkg
        lines.append(f'rectangle "{label}" as {alias}')

    for pkg, deps in graph.items():
        src_alias = _safe_alias(pkg)
        for dep in deps:
            dst_alias = _safe_alias(dep)
            lines.append(f"{src_alias} --> {dst_alias}")

    lines.append("@enduml")
    return "\n".join(lines)


def save_graph_svg(puml_text: str, output_path: str) -> None:
    """Генерирует SVG-изображение по коду PlantUML и сохраняет в файл."""
    encoded = encode_plantuml_text(puml_text)
    url = PLANTUML_SVG_URL + encoded
    try:
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as resp:
            svg_bytes = resp.read()
    except Exception as err:
        raise RuntimeError(f"Ошибка генерации SVG: {err}") from err

    with open(output_path, "wb") as out_file:
        out_file.write(svg_bytes)
