import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

if load_dotenv is not None:
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

SPARK_BATCH_SIZE = int(os.getenv("SPARK_BATCH_SIZE"))

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT_INTERNAL")
