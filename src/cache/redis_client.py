import json 
import redis
from utils.logger import get_logger
from config.settings import REDIS_HOST, REDIS_PORT


class RedisClient:

    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )
        self.logger = get_logger("REDIS")
    
        try:
            self.redis_client.ping()
            self.logger.info("Connected to Redis.")
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            raise

    def set(self, key: str, value: dict):
        try:
            self.redis_client.set(key, json.dumps(value))
        except Exception as e:
            self.logger.error(f"Error setting key {key} in Redis: {e}")

    def get(self, key: str):
        try:
            value = self.redis_client.get(key)
            if value is not None:
                return json.loads(value)
            return None
        except Exception as e:
            self.logger.error(f"Error getting key {key} from Redis: {e}")
            return None

    def get_keys(self, pattern: str):
        try:
            return self.redis_client.keys(pattern)
        except Exception as e:
            self.logger.error(f"Error getting keys from Redis: {e}")
            return []