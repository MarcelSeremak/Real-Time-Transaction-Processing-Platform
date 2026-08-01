import os
from dotenv import load_dotenv

load_dotenv()


CUSTOMER_RATE = int(
    os.getenv("CUSTOMER_RATE")
)

KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")

CUSTOMER_TOPIC = "customers"
