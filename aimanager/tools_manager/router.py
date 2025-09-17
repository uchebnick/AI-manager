from typing import Callable

class ToolsRouter:
    _tools: dict[str, Callable] = {}
    _tools_json: list[dict] = []
    _lib_env: dict = {}

    def __init__(self, lib_name: str, tools_json: list[dict] = None):
        self.lib_name: str = lib_name
        if tools_json:
            self._tools_json.extend(tools_json)



    def tool(self, tool_name: str = None, tool_json: dict = None):
        def decorator(func: Callable):
            name_to_register = tool_name if tool_name is not None else func.__name__
            full_name = f'{self.lib_name}.{name_to_register}'
            self._tools[full_name] = func
            if tool_json:
                self._tools_json.append(tool_json)
            return func

        return decorator

    @classmethod
    def get_tools_json(cls) -> list[dict]:
        return cls._tools_json

    @classmethod
    def get_tool(cls, name: str) -> Callable | None:
        return cls._tools.get(name)
