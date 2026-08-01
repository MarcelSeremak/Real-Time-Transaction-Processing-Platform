from faker import Faker
from generator.base import BaseGenerator

class MerchantGenerator(BaseGenerator):

    def __init__(
        self,
        rate_per_second: int,
        bootstrap_server: str,
        topic: str
    ):
        super().__init__(
            rate_per_second,
            bootstrap_server,
            topic
        )
        self.fake = Faker()

    def generate(self):
        return {
            "merchant_name": self.fake.company(),
            "category": self.fake.random_element(
                [
                    "GROCERY",
                    "ELECTRONICS",
                    "CLOTHING",
                    "RESTAURANT",
                    "TRAVEL"
                ]
            ),
            "country": self.fake.country(),
            "city": self.fake.city(),
            "status": "ACTIVE"
        }