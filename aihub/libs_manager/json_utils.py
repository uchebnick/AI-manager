import json
import logging
import os
from dataclasses import asdict
from typing import Iterator, Literal

from .lib import Library

lib_json_path = "aihub/libs.json"
logger = logging.getLogger(__name__)


def add_library(lib: Library) -> None:
    """
    Добавляет или обновляет библиотеку в файле libs.json.

    Если библиотека с таким же именем уже существует, она будет обновлена.
    В противном случае новая библиотека будет добавлена в список.
    """
    data = {"libraries": []}
    if os.path.exists(lib_json_path):
        try:
            with open(lib_json_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    data = json.loads(content)
                if not isinstance(data.get("libraries"), list):
                    data["libraries"] = []
        except (json.JSONDecodeError, FileNotFoundError):
            logger.warning(
                f"File '{lib_json_path}' not found or is corrupted. A new file will be created."
            )
            data = {"libraries": []}

    lib_as_dict = asdict(lib)
    libraries = data["libraries"]

    found_index = -1
    for i, existing_lib in enumerate(libraries):
        if isinstance(existing_lib, dict) and existing_lib.get("name") == lib.name:
            found_index = i
            break

    if found_index != -1:
        logger.info(f"Updating library '{lib.name}' in '{lib_json_path}'.")
        libraries[found_index] = lib_as_dict  # Обновить существующую
    else:
        logger.info(f"Adding new library '{lib.name}' to '{lib_json_path}'.")
        libraries.append(lib_as_dict)  # Добавить новую

    with open(lib_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def get_libraries(type: Literal["tool", "trigger"] = None) -> Iterator[Library]:
    """
    Читает libs.json и возвращает итератор объектов Library.
    Можно отфильтровать по типу ('tool' или 'trigger').
    """
    if not os.path.exists(lib_json_path):
        logger.warning(f"Library file not found at '{lib_json_path}'.")
        return

    try:
        with open(lib_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        libraries_data = data.get("libraries", [])
        if not isinstance(libraries_data, list):
            logger.warning(f"Key 'libraries' in '{lib_json_path}' is not a list.")
            return

        for lib_data in libraries_data:
            if type is None or lib_data.get("type") == type:
                try:
                    yield Library(**lib_data)
                except TypeError:
                    logger.warning(
                        f"Skipping malformed library data in '{lib_json_path}': {lib_data}"
                    )
                    continue
    except (json.JSONDecodeError, FileNotFoundError):
        logger.error(f"Failed to read or parse '{lib_json_path}'.")
        return
