from typing import Any, Callable, Dict, List

from aihub.tools_manager.manager import ToolManager, tool_manager


class LLMHub:
    """
    Класс-хаб для управления и регистрации инструментов (tools) для больших языковых моделей (LLM).
    Позволяет регистрировать функции как инструменты с помощью декоратора.
    """
    def __init__(self, lib_name: str, manager: ToolManager = tool_manager, tools_json: List[Dict[str, Any]] = None):
        """
        Инициализирует экземпляр LLMHub.

        :param lib_name: Имя библиотеки, к которой будут относиться регистрируемые инструменты.
        :param manager: Экземпляр менеджера инструментов, который будет использоваться для регистрации.
        :param tools_json: Список словарей с описанием инструментов в формате JSON для массовой регистрации.
        """
        self.lib_name: str = lib_name
        self.tool_manager: ToolManager = manager
        if tools_json:
            # Если предоставлен список инструментов в формате JSON, регистрируем их
            self.tool_manager.register_tools_json(tools_json)

    def tool(self, tool_name: str = None, tool_json: Dict[str, Any] = None):
        """
        Декоратор для регистрации функции в качестве инструмента.

        :param tool_name: Необязательное имя для инструмента. Если не указано, используется имя функции.
        :param tool_json: Необязательный словарь с JSON-описанием инструмента.
        :return: Декоратор.
        """
        def decorator(func: Callable):
            # Если имя инструмента не предоставлено, используем имя самой функции
            name_to_register = tool_name if tool_name is not None else func.__name__
            # Создаем полное имя инструмента в формате 'имя_библиотеки.имя_инструмента'
            full_name = f"{self.lib_name}.{name_to_register}"
            # Регистрируем инструмент в менеджере
            self.tool_manager.register_tool(full_name, func, tool_json)
            return func
        return decorator
