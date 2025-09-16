class LLMContext:
    def __init__(self):
        self.messages = []

    def add_user_message(self, message_content: str):
        """Adds a user message to the context."""
        user_message = {
            "role": "user",
            "content": message_content
        }
        self.messages.append(user_message)

    def add_ai_message(self, message_content: str):
        """Adds an AI (assistant) message to the context."""
        ai_message = {
            "role": "assistant",
            "content": message_content
        }
        self.messages.append(ai_message)

    def get_context(self) -> list:
        """
        Returns the full conversation context as a list of message dictionaries.
        This is the format commonly used by LLM APIs.
        """
        return self.messages

    def clear_context(self):
        """Clears the entire conversation history."""
        self.messages = []
        print("Context cleared.")

