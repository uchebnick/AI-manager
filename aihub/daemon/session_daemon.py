from aihub.session import LLMContext
from aihub.triggers_manager.message_queue import RedisQueue


class SessionDaemon:
    """
    Демон сессии, отвечающий за управление контекстом LLM и обработку сообщений из очереди.
    """
    def __init__(self, session_id: str, context: LLMContext, queue: RedisQueue):
        """
        Инициализирует экземпляр SessionDaemon.

        :param session_id: Уникальный идентификатор сессии.
        :param context: Экземпляр LLMContext для управления историей диалога.
        :param queue: Экземпляр RedisQueue для получения входящих сообщений.
        """
        self.session_id = session_id
        self.context = context
        self.queue = queue

    def _check_triggers(self):
        # TODO: Реализовать логику проверки триггеров
        pass

    def _next_gen(self):
        """
        Извлекает следующее сообщение из очереди и добавляет его в контекст пользователя.
        """
        message = self.queue.pop()
        if not message:
            return None
        self.context.add_user_message(message)
