import json
import time

import redis


class RedisQueue:
    """
    Класс для реализации очереди в Redis, где каждый элемент
    имеет свое собственное время жизни (TTL).
    """

    def __init__(self, redis_conn: redis.Redis, queue_name: str):
        """
        Инициализирует очередь.

        :param redis_conn: Активное соединение с Redis (объект redis.Redis).
        :param queue_name: Имя ключа в Redis, который будет использоваться для очереди.
        """
        if not isinstance(redis_conn, redis.Redis):
            raise TypeError("redis_conn должен быть экземпляром redis.Redis")
        self.redis = redis_conn
        self.queue_name = queue_name

    def push(self, item: any, ttl_seconds: int):
        """
        Добавляет элемент в начало очереди с указанным временем жизни.

        :param item: Элемент для добавления (может быть любого типа,
                     который сериализуется в JSON).
        :param ttl_seconds: Время жизни элемента в секундах.
        """
        # Рассчитываем время, когда элемент "протухнет"
        expires_at = time.time() + ttl_seconds

        # Упаковываем данные и время истечения в словарь
        payload = {"data": item, "expires_at": expires_at}

        # Сериализуем в JSON и добавляем в начало списка (LPUSH)
        self.redis.lpush(self.queue_name, json.dumps(payload))
        print(f"✅ Добавлен элемент: {item} (TTL: {ttl_seconds} сек)")

    def pop(self) -> any:
        """
        Извлекает и возвращает самый старый валидный элемент из конца очереди.

        Если самый старый элемент просрочен, он удаляется, и делается
        попытка извлечь следующий. Процесс повторяется, пока не будет
        найден валидный элемент или очередь не опустеет.

        :return: Данные элемента или None, если очередь пуста.
        """
        while True:
            # Атомарно извлекаем элемент с конца списка (RPOP)
            serialized_payload = self.redis.rpop(self.queue_name)

            if serialized_payload is None:
                # Очередь пуста
                return None

            payload = json.loads(serialized_payload)

            # Проверяем, не истекло ли время жизни элемента
            if time.time() < payload["expires_at"]:
                # Элемент валиден, возвращаем его данные
                print(f"🔷 Извлечен валидный элемент: {payload['data']}")
                return payload["data"]
            else:
                # Элемент просрочен, он просто игнорируется
                print(f"❌ Элемент {payload['data']} просрочен и удален.")
                # Цикл продолжится, чтобы проверить следующий элемент

    def size(self) -> int:
        """
        Возвращает текущий размер очереди (включая просроченные элементы,
        которые еще не были извлечены).

        :return: Количество элементов в списке Redis.
        """
        return self.redis.llen(self.queue_name)

    def is_empty(self) -> bool:
        """
        Проверяет, пуста ли очередь.

        :return: True, если очередь пуста, иначе False.
        """
        return self.size() == 0
