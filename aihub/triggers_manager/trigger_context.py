from datetime import datetime

from aimanager.triggers_manager.message_queue import RedisQueue


class TriggerContext:
    """
    Предоставляет контекст и утилиты для триггеров в момент их проверки.
    Экземпляр этого класса создается для каждого цикла проверки триггеров.
    """

    def __init__(self, session_id: str, lib_env: dict, queue: RedisQueue):
        self.session_id: str = session_id
        self.lib_env: dict = lib_env

        self._check_time: datetime = datetime.now()
        self._queue: RedisQueue = queue

    def get_check_time(self) -> datetime:
        """Возвращает время начала текущего цикла проверки триггеров."""
        return self._check_time

    def get_k8s_manager(self):
        """Возвращает менеджер Kubernetes для управления ресурсами."""
        # TODO: Реализовать получение менеджера Kubernetes
        pass

    def push_message(self, message: str, ttl: int = 300):
        """Отправляет сообщение в очередь для обработки LLM."""
        self._queue.push(message, ttl)

    def llm_chat(self, message: str):
        """Вызов LLM для генерации ответа на сообщение."""
        # TODO: Реализовать вызов LLM
        pass
