# app/utils.py
import os
import json
import asyncio
import logging
import redis.asyncio as redis

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# не создаём клиент на уровне импорта, сделаем лениво
_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        # socket_connect_timeout уменьшит время ожидания при недоступном сервере
        _redis_client = redis.from_url(REDIS_URL, socket_connect_timeout=2)
    return _redis_client

async def get_cache(key: str, timeout: float = 2.0):
    """
    Попытка получить значение из Redis, но с ограничением по времени.
    Возвращает None при ошибке / таймауте.
    """
    client = get_redis_client()
    try:
        data = await asyncio.wait_for(client.get(key), timeout=timeout)
        if data:
            try:
                print('get', data)
                return json.loads(data)
            except Exception:
                return None
        return None
    except asyncio.TimeoutError:
        logger.warning("Redis get timeout for key=%s", key)
        return None
    except Exception as e:
        logger.warning("Redis get error: %s", e)
        return None

async def set_cache(key: str, value: dict, ttl: int = 600, timeout: float = 2.0):
    client = get_redis_client()
    try:
        payload = json.dumps(value)
        print('set', payload)
        # асинхронная установка с ограничением по времени
        await asyncio.wait_for(client.set(key, payload, ex=ttl), timeout=timeout)
    except asyncio.TimeoutError:
        logger.warning("Redis set timeout for key=%s", key)
    except Exception as e:
        logger.warning("Redis set error: %s", e)
