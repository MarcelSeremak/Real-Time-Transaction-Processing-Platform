from abc import ABC, abstractmethod
import uuid
from datetime import datetime, timezone
from threading import Event
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
        self.stop_event = Event()

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def send(self, event):
        pass

    def create_event(self, data: dict):
        return {
            "event_id": str(uuid.uuid4()),
            "event_type": self.__class__.__name__,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        }
    def stop(self):
        self.stop_event.set()
        self.logger.info(f"Stopping generator {self.__class__.__name__}")

    def run(self):
        delay = 1 / self.rate_per_second

        self.logger.info(
            f"Starting generator {self.__class__.__name__} "
            f"with rate {self.rate_per_second}/s"
        )

        while not self.stop_event.is_set():
            try:
                data = self.generate()
                if data is None:
                    self.stop_event.wait(delay)
                    continue

                event = self.create_event(data)
                self.send(event)
                self.counter += 1
                if self.counter % 100 == 0:
                    self.logger.info(f"{self.__class__.__name__} generated {self.counter} events")
            except Exception:
                self.logger.exception(f"{self.__class__.__name__} failed")
                raise

            self.stop_event.wait(delay)
