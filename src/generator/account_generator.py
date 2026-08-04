from faker import Faker
from uuid import uuid4
from generator.base import BaseGenerator

class AccountGenerator(BaseGenerator):

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
        customers = self.cache.get_keys(
            "customer:*"
        )
        if not customers:
            return None
        customer_key = self.fake.random_element(customers)
        customer = self.cache.get(customer_key)
        account_id = str(uuid4())

        account = {
            "account_id": account_id,
            "customer_id": customer["customer_id"],
            "iban": self.fake.iban(),
            "currency": self.fake.random_element(
                [
                    "PLN",
                    "EUR",
                    "USD"
                ]
            ),
            "balance": round(
                self.fake.pyfloat(
                    min_value=0,
                    max_value=10000
                ),
                2
            ),
            "status": "ACTIVE"
        }
        self.cache.set(
            f"account:{account_id}",
            account
        )

        return account
    
    def send(self, event):
        self.producer.send(event,
                        key=event["data"]["account_id"])
