import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from generator.customer_generator import CustomerGenerator
from config.settings import (
    CUSTOMER_RATE,
    KAFKA_BOOTSTRAP_SERVER
)


generator = CustomerGenerator(
    rate_per_second=CUSTOMER_RATE,
    bootstrap_server=KAFKA_BOOTSTRAP_SERVER,
    topic="customers"
)

generator.run()