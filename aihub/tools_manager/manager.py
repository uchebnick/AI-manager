from typing import Any, Callable, Dict, List


class ToolManager:
    """
    Менеджер инструментов для регистрации, получения и управления инструментами (функциями)
    и их JSON-описаниями, которые могут использоваться большими языковыми моделями (LLM).
    """
    def __init__(self):
        # Словарь для хранения зарегистрированных функций-инструментов, где ключ - имя инструмента, значение - функция.
        self.tools: dict[str, Callable] = {}
        # Словарь для хранения JSON-описаний инструментов, где ключ - имя инструмента, значение - JSON-схема.
        self.tools_json: dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, tool: Callable, tool_json: Dict[str, Any] = None):
        """
        Регистрирует функцию в качестве инструмента.

        :param name: Уникальное имя инструмента.
        :param tool: Сама функция, которая будет зарегистрирована как инструмент.
        :param tool_json: Необязательное JSON-описание инструмента.
        """
        self.tools[name] = tool
        if tool_json:
            self.tools_json[name] = tool_json

    def get_tool(self, name: str) -> Callable | None:
        """
        Возвращает зарегистрированный инструмент по его имени.

        :param name: Имя инструмента.
        :return: Зарегистрированная функция или None, если инструмент не найден.
        """
        return self.tools.get(name)

    def list_tools(self) -> List[str]:
        """
        Возвращает список имен всех зарегистрированных инструментов.

        :return: Список строк с именами инструментов.
        """
        return list(self.tools.keys())

    def get_tool_json(self, tool_name: str) -> Dict[str, Any] | None:
        """
        Возвращает JSON-описание инструмента по его имени.

        :param tool_name: Имя инструмента.
        :return: Словарь с JSON-описанием инструмента или None, если описание не найдено.
        """
        return self.tools_json.get(tool_name)

    def get_all_tools_json(self) -> List[Dict[str, Any]]:
        """
        Возвращает список всех зарегистрированных JSON-описаний инструментов.

        :return: Список словарей с JSON-описаниями инструментов.
        """
        return list(self.tools_json.values())

    def register_tools_json(self, tools_json: List[Dict[str, Any]]):
        """
        Регистрирует несколько инструментов на основе списка их JSON-описаний.

        :param tools_json: Список словарей, каждое из которых является JSON-описанием инструмента.
        """
        new_schemas = {
            tool_spec["name"]: tool_spec
            for tool_spec in tools_json
            if isinstance(tool_spec, dict) and "name" in tool_spec
        }
        self.tools_json.update(new_schemas)

# Создаем глобальный экземпляр ToolManager для использования во всем приложении.
tool_manager = ToolManager()
