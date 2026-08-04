import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


CUSTOMER_RATE = int(
    os.getenv("CUSTOMER_RATE")
)
ACCOUNT_RATE = int(
    os.getenv("ACCOUNT_RATE")
)
MERCHANT_RATE = int(
    os.getenv("MERCHANT_RATE")
)
TRANSACTION_RATE = int(
    os.getenv("TRANSACTION_RATE")
)

KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")

CUSTOMER_TOPIC = "customers"
ACCOUNT_TOPIC = "accounts"
MERCHANT_TOPIC = "merchants"
TRANSACTION_TOPIC = "transactions"

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
