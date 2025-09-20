import logging

from .lib_runner import run_tools_libs
from .router.make_global import make_package_global

# Точка входа для запуска менеджера инструментов.
if __name__ == "__main__":
    # Инициализация логгера для главного модуля.
    logger = logging.getLogger(__name__)

    logger.info("Запуск глобальной настройки пакета...")
    # Выполняем глобальную установку пакета router_lib.
    make_package_global()
    logger.info("Глобальная настройка пакета завершена.")

    logger.info("Запуск загрузчика библиотек инструментов...")
    # Запускаем функцию для загрузки и регистрации библиотек инструментов.
    run_tools_libs()
    logger.info("Загрузчик библиотек инструментов завершил работу.")
