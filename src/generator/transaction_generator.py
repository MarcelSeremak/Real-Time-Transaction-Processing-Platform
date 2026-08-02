from faker import Faker
from uuid import uuid4
from generator.base import BaseGenerator

class TransactionGenerator(BaseGenerator):

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
        accounts = self.cache.get_keys(
            "account:*"
        )
        merchants = self.cache.get_keys(
            "merchant:*"
        )
        if not accounts or not merchants:
            return {
                "error": "Missing account or merchant"
            }

        account = self.cache.get(
            self.fake.random_element(accounts)
        )

        merchant = self.cache.get(
            self.fake.random_element(merchants)
        )

        transaction_id = str(uuid4())
        return {
            "transaction_id": transaction_id,
            "account_id": account["account_id"],
            "merchant_id": merchant["merchant_id"],
            "amount": round(
                self.fake.pyfloat(
                    min_value=1,
                    max_value=5000
                ),
                2 
            ),
            "currency": account["currency"],
            "transaction_type": self.fake.random_element(
                [
                    "PAYMENT",
                    "TRANSFER",
                    "WITHDRAWAL"
                ]
            ),
            "status": "COMPLETED"
        }