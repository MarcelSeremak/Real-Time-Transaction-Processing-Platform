import json
from kafka import KafkaProducer


class KafkaGenerator:

    def __init__(self, bootstrap_server: str, topic: str):
        self.topic = topic
        bootstrap_servers = [
            server.strip()
            for server in bootstrap_server.split(",")
            if server.strip()
        ]

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            retries=5,
            linger_ms=10,
            enable_idempotence=True,
            compression_type="lz4",
        )

    def send(self, message: dict, key: str = None):
        self.producer.send(self.topic,
                            key=key.encode("utf-8") if key else None,
                            value=message)

    def close(self):
        self.producer.flush()
        self.producer.close()
