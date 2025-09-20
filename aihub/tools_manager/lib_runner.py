import logging
import os
import subprocess
import sys

from aihub.libs_manager import get_libraries

# Инициализация логгера для модуля lib_runner
logger = logging.getLogger("aihub.tools_manager.lib_runner")









def run_tools_libs():
    """
    Запускает библиотеки типа 'tool', которые указаны в aihub/libs.
    Запуск производится через 'python -m aihub.libs.<name>' для корректного исполнения пакета.
    """
    # Получаем корневую директорию, где находятся библиотеки.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    libs_path = os.path.abspath(os.path.join(script_dir, '..', 'libs'))

    # Проходим по всем библиотекам типа 'tool'
    for lib_data in get_libraries(type="tool"):
        # Пропускаем библиотеки, которые не отмечены как работоспособные
        if not lib_data.is_work:
            logger.debug(f"Пропуск библиотеки '{lib_data.name}', так как она помечена как нерабочая.")
            continue

        lib_path = os.path.join(libs_path, lib_data.name)

        # Проверяем, существует ли директория библиотеки
        if not os.path.isdir(lib_path):
            logger.error(f"Директория не найдена по пути '{lib_path}'")
            continue

        logger.info(f"Запуск библиотеки-инструмента: '{lib_data.name}' из '{lib_path}'")

        # Формируем модульное имя для запуска через -m: aihub.libs.<name>
        module_name = f"aihub.libs.{lib_data.name}"

        try:
            # Запускаем пакет как модуль: python -m aihub.libs.<name>
            result = subprocess.run(
                [sys.executable, "-m", module_name],
                capture_output=True,
                text=True,
                check=False  # Проверяем returncode вручную
            )

            if result.returncode == 0:
                logger.info(f"Успешный запуск '{lib_data.name}'.")
                if result.stdout:
                    logger.info(f"Вывод от '{lib_data.name}':\n{result.stdout}")
            else:
                logger.error(f"Ошибка при запуске '{lib_data.name}'. Код возврата: {result.returncode}")
                if result.stderr:
                    logger.error(f"Ошибка (stderr) от '{lib_data.name}':\n{result.stderr}")

        except Exception as e:
            logger.exception(f"Исключение при попытке запустить библиотеку '{lib_data.name}': {e}")
