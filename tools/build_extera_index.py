"""Собирает extera-plugins.json — манифест каталога плагинов exteraGram.

Сканирует *.plugin в корне репозитория дистрибуции, вытаскивает метаданные
из шапки каждого плагина (AST-парс верхнего уровня), считает sha256/size и
записывает индекс. Запуск: python build_index.py [root_dir].

Правило каталога: id и version в манифесте обязаны совпадать с метаданными
внутри .plugin, а sha256/size — с реальным файлом. После любого изменения
.plugin индекс нужно пересобрать (это же делает GitHub Actions).
"""
import ast
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_NAME = "extera-plugins.json"

DEFAULT_CATEGORY = ["tools"]


def _literal_assignments(tree: ast.Module) -> dict:
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                values[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                pass
    return values


def parse_plugin_meta(path: Path) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    meta = _literal_assignments(tree)

    plugin_id = str(meta.get("__id__", path.stem)).strip()
    version = str(meta.get("__version__", "1.0")).strip()
    if not version:
        version = "1.0"
    if not plugin_id:
        raise ValueError(f"{path.name}: пустой __id__")

    app_version = str(meta.get("__app_version__") or meta.get("__min_version__") or "").strip()
    sdk_version = str(meta.get("__sdk_version__") or "").strip()
    category = meta.get("__category__") or DEFAULT_CATEGORY
    if isinstance(category, str):
        category = [category]
    category = [str(c).strip() for c in category][:3]

    entry = {
        "id": plugin_id,
        "name": str(meta.get("__name__", plugin_id)).strip(),
        "description": str(meta.get("__description__", "")).strip(),
        "author": str(meta.get("__author__", "")).strip(),
        "version": version,
        "category": category,
        "file": path.name,
    }
    if app_version:
        entry["app_version"] = app_version if app_version.startswith((">", "<", "=")) else f">={app_version}"
    if sdk_version:
        entry["sdk_version"] = sdk_version if sdk_version.startswith((">", "<", "=")) else f">={sdk_version}"
    icon = str(meta.get("__icon__", "")).strip()
    if icon:
        entry["icon"] = icon
    return entry


def build_index(root: Path) -> dict:
    plugins = []
    for path in sorted(root.glob("*.plugin")):
        if path.name == MANIFEST_NAME:
            continue
        data = path.read_bytes()
        entry = parse_plugin_meta(path)
        entry["sha256"] = hashlib.sha256(data).hexdigest()
        entry["size"] = len(data)
        entry["updated_at"] = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        plugins.append(entry)
        print(f"  + {entry['id']} v{entry['version']} ({entry['size']} байт, sha256 {entry['sha256'][:12]}…)")

    return {
        "schema": 1,
        "name": "Good Proxies",
        "description": "Сборщик рабочих прокси, замер скорости и крипто-проверки для exteraGram.",
        "author": "@MouXoziain",
        "homepage": "https://github.com/Iliya3ProX/good_proxies",
        "plugins": plugins,
    }


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    index = build_index(root)
    out = root / MANIFEST_NAME
    out.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{MANIFEST_NAME}: {len(index['plugins'])} плагинов -> {out}")


if __name__ == "__main__":
    main()
