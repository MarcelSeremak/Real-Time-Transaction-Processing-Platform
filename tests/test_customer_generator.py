from unittest.mock import patch
from uuid import UUID

from generator.customer_generator import CustomerGenerator


def test_generator_data_logic():

    with patch("generator.base.KafkaGenerator"), \
         patch("generator.base.RedisClient"):

        generator = CustomerGenerator(
            10,
            "localhost:29092",
            "customers"
        )

        customer = generator.generate()

        assert "customer_id" in customer
        assert "first_name" in customer
        assert "last_name" in customer
        assert "risk_level" in customer
        assert "status" in customer
        assert isinstance(UUID(customer["customer_id"]), UUID)

def test_generator_cache_logic():

    with patch("generator.base.KafkaGenerator"), \
         patch("generator.base.RedisClient"):

        generator = CustomerGenerator(
            10,
            "localhost:29092",
            "customers"
        )

        customer = generator.generate()

        generator.cache.set.assert_called_once_with(
            f"customer:{customer['customer_id']}",
            customer
        )

def test_generator_kafka_logic():
    
    with patch("generator.base.KafkaGenerator"), \
         patch("generator.base.RedisClient"):

        generator = CustomerGenerator(
            10,
            "localhost:29092",
            "customers"
        )

        customer = generator.generate()
        event = generator.create_event(customer)

        generator.send(event)

        generator.producer.send.assert_called_once_with(
            event,
            key=event["data"]["customer_id"]
        )