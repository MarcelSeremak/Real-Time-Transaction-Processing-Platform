from pyspark.sql import SparkSession
from pyspark.sql.streaming import StreamingQuery

from spark.reader import read_events
from spark.schema import (
    account_schema,
    customer_schema,
    merchant_schema,
    transaction_schema,
)
from spark.transformer import (
    clean_events,
    project_for_table,
    transform_events,
)
from spark.writer import write_to_postgres
from utils.logger import get_logger

logger = get_logger("SPARK_JOB")

EVENT_CONFIG = {
    "accounts": {
        "event_type": "AccountGenerator",
        "schema": account_schema,
        "table": "accounts",
    },
    "customers": {
        "event_type": "CustomerGenerator",
        "schema": customer_schema,
        "table": "customers",
    },
    "merchants": {
        "event_type": "MerchantGenerator",
        "schema": merchant_schema,
        "table": "merchants",
    },
    "transactions": {
        "event_type": "TransactionGenerator",
        "schema": transaction_schema,
        "table": "transactions",
    },
}


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("TransactionPipeline")
        .getOrCreate()
    )


def process_event(
    spark: SparkSession,
    topic: str,
    config: dict,
) -> StreamingQuery:

    df = read_events(
        spark,
        topic
    )

    df = transform_events(
        df,
        config["schema"]
    )

    df = clean_events(
        df,
        config["event_type"]
    )

    df = project_for_table(
        df,
        config["table"]
    )

    def write_batch(batch_df, batch_id):
        try:
            write_to_postgres(batch_df, config["table"])
        except Exception:
            logger.exception(
                f"Failed writing batch {batch_id} for {config['table']}, "
                "batch dropped, streaming continues"
            )

    query = (
        df.writeStream
        .foreachBatch(write_batch)
        .option(
            "checkpointLocation",
            f"checkpoints/{topic}"
        )
        .start()
    )

    return query


def main() -> None:

    spark = create_spark_session()

    queries = []

    try:
        for topic, config in EVENT_CONFIG.items():
            query = process_event(
                spark,
                topic,
                config
            )
            queries.append(query)

        for query in queries:
            query.awaitTermination()

    finally:
        spark.stop()


if __name__ == "__main__":
    main()