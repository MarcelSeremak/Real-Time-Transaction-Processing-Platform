from abc import ABC, abstractmethod
import time
import uuid
from datetime import datetime, timezone
from cache import RedisClient
from kafka_producer import KafkaGenerator
from utils.logger import get_logger


class BaseGenerator(ABC):

    def __init__(self, rate_per_second: int, bootstrap_server: str, topic: str):
        self.rate_per_second = rate_per_second
        self.logger = get_logger(self.__class__.__name__)
        self.producer = KafkaGenerator(
            bootstrap_server,
            topic
        )
        self.cache = RedisClient()
        self.counter = 0

    @abstractmethod
    def generate(self):
        pass

    def create_event(self, data: dict):
        return {
            "event_id": str(uuid.uuid4()),
            "event_type": self.__class__.__name__,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        }

    def run(self):
        delay = 1 / self.rate_per_second

        self.logger.info(
            f"Starting generator {self.__class__.__name__} "
            f"with rate {self.rate_per_second}/s"
        )

        while True:
            event = self.create_event(
                self.generate()
            )

            self.send(event)
            self.counter += 1
            if self.counter % 100 == 0:
                self.logger.info(f"{self.__class__.__name__} generated {self.counter} events")
            time.sleep(delay)

    def send(self, event):
        self.producer.send(event)