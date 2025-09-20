class LLMContext:
    def __init__(self):
        # Инициализация списка для хранения сообщений диалога
        self.messages = []

    def add_user_message(self, message_content: str):
        """Добавляет сообщение пользователя в контекст."""
        user_message = {"role": "user", "content": message_content}
        self.messages.append(user_message)

    def add_ai_message(self, message_content: str):
        """Добавляет сообщение AI (ассистента) в контекст."""
        ai_message = {"role": "assistant", "content": message_content}
        self.messages.append(ai_message)

    def get_context(self) -> list:
        """
        Возвращает полный контекст разговора в виде списка словарей сообщений.
        Этот формат обычно используется API больших языковых моделей (LLM).
        """
        return self.messages

    def clear_context(self):
        """Очищает всю историю разговора."""
        self.messages = []
        print("Контекст очищен.")
