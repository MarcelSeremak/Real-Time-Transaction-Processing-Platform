import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

sys.path.append(str(Path(__file__).parent.parent))

from generator.customer_generator import CustomerGenerator
from generator.merchant_generator import MerchantGenerator
from generator.account_generator import AccountGenerator
from generator.transaction_generator import TransactionGenerator
from config.settings import (
    CUSTOMER_RATE,
    MERCHANT_RATE,
    ACCOUNT_RATE,
    TRANSACTION_RATE,
    KAFKA_BOOTSTRAP_SERVER
)


customer_generator = CustomerGenerator(
    rate_per_second=CUSTOMER_RATE,
    bootstrap_server=KAFKA_BOOTSTRAP_SERVER,
    topic="customers"
)

merchant_generator = MerchantGenerator(
    rate_per_second=MERCHANT_RATE,
    bootstrap_server=KAFKA_BOOTSTRAP_SERVER,
    topic="merchants"
)

account_generator = AccountGenerator(
    rate_per_second=ACCOUNT_RATE,
    bootstrap_server=KAFKA_BOOTSTRAP_SERVER,
    topic="accounts"
)

transaction_generator = TransactionGenerator(
    rate_per_second=TRANSACTION_RATE,
    bootstrap_server=KAFKA_BOOTSTRAP_SERVER,
    topic="transactions"
)

generators = [
    customer_generator,
    merchant_generator,
    account_generator,
    transaction_generator
]

with ThreadPoolExecutor(max_workers=len(generators)) as executor:
    for generator in generators:
        executor.submit(generator.run)