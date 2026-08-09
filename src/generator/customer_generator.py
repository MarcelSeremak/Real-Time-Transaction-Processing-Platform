from uuid import uuid4

from faker import Faker

from generator.base import BaseGenerator


class CustomerGenerator(BaseGenerator):

    def __init__(self, rate_per_second: int,
                bootstrap_server: str,
                topic: str
            ):
        super().__init__(rate_per_second, bootstrap_server, topic)
        self.fake = Faker()

    def generate(self):


        customer_id = str(uuid4())

        customer = {
            "customer_id": customer_id,
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "country": self.fake.country(),
            "city": self.fake.city(),
            "risk_level": self.fake.random_element(
                ["LOW", "MEDIUM", "HIGH"]
            ),
            "status": "ACTIVE"
        }
 
        self.cache.set(
            f"customer:{customer_id}",
            customer
        )

        return customer

    def send(self, event):
        self.producer.send(event,
                        key=event["data"]["customer_id"])