import signal
import sys
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import (
    ACCOUNT_RATE,
    CUSTOMER_RATE,
    KAFKA_BOOTSTRAP_SERVER,
    MERCHANT_RATE,
    TRANSACTION_RATE,
)
from generator.account_generator import AccountGenerator
from generator.customer_generator import CustomerGenerator
from generator.merchant_generator import MerchantGenerator
from generator.transaction_generator import TransactionGenerator

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

def shutdown(signal_number, frame):
    print("Received shutdown signal. Stopping generators...")
    for generator in generators:
        generator.stop()

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

executor = ThreadPoolExecutor(
    max_workers=len(generators)
)

with executor as executor:
    futures = {
        executor.submit(generator.run): generator
        for generator in generators
    }
    done, _ = wait(futures, return_when=FIRST_EXCEPTION)
    for future in done:
        exception = future.exception()
        if exception:
            generator = futures[future]
            print(f"{generator.__class__.__name__} encountered an error: {exception}")
            shutdown(None, None)
            raise exception
