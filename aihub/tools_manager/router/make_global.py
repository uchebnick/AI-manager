import logging
import os
import subprocess
import sys

# Инициализация логгера для модуля make_global
logger = logging.getLogger("tools_manager.router.make_global")

def make_package_global():
    """
    Устанавливает пакет из директории 'router_lib' в режиме редактирования (editable mode).
    Это позволяет вносить изменения в код пакета без переустановки.
    """
    try:
        # Получаем абсолютный путь к директории, содержащей этот скрипт.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Формируем путь к директории пакета router_lib.
        package_path = os.path.abspath(os.path.join(script_dir, '..', 'router_lib'))

        # Проверяем, существует ли указанная директория пакета.
        if not os.path.isdir(package_path):
            logger.error(f"Директория не найдена по пути '{package_path}'")
            sys.exit(1)

        logger.info(f"Установка пакета из '{package_path}' в режиме редактирования...")

        # Используем sys.executable, чтобы гарантировать использование pip из текущего окружения Python.
        command = [sys.executable, "-m", "pip", "install", "-e", "."]

        # Запускаем команду в директории пакета.
        result = subprocess.run(
            command,
            cwd=package_path,
            check=True, # Вызывает исключение CalledProcessError, если команда возвращает ненулевой код выхода.
            capture_output=True, # Захватывает stdout и stderr.
            text=True # Декодирует stdout и stderr как текст.
        )

        logger.info("Установка прошла успешно.")
        logger.info(f"Вывод pip:\n{result.stdout}")

    except FileNotFoundError:
        logger.critical("Команда 'python' или 'pip' не найдена.")
        logger.critical("Пожалуйста, убедитесь, что Python и pip установлены и находятся в переменной PATH вашей системы.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        logger.error("Ошибка во время установки.")
        logger.error(f"Код возврата: {e.returncode}")
        logger.error(f"Вывод:\n{e.stdout}")
        logger.error(f"Вывод ошибок:\n{e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    # Если скрипт запускается напрямую, выполняем установку пакета.
    make_package_global()
