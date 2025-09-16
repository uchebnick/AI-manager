from pyexpat.errors import messages

from aimanager.session import LLMContext
from aimanager.utils import gen_random_string
from aimanager.message_queue import RedisQueue

class Daemon:
    def __init__(self, session_id: str, context: LLMContext, queue: RedisQueue):
        self.session_id = session_id
        self.context = context
        self.queue = queue

    def _check_triggers(self):


    def _next_gen(self):
        message = self.queue.pop()
        if not message:
            return None
        self.context.add_user_message(message)


