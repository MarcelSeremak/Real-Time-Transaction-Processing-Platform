from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    from_json,
    to_timestamp,
)
from pyspark.sql.types import StructType


def transform_events(
    df: DataFrame,
    schema: StructType
) -> DataFrame:

    return (
        df
        .select(
            from_json(
                col("value").cast("string"),
                schema
            ).alias("event")
        )
        .select(
            "event.event_id",
            "event.event_type",
            "event.timestamp",
            "event.data.*"
        )
    )


def clean_events(
    df: DataFrame,
    event_type: str
) -> DataFrame:

    df = (
        df
        .withColumn(
            "timestamp",
            to_timestamp("timestamp")
        )
        .filter(
            col("event_id").isNotNull()
        )
        .filter(
            col("timestamp").isNotNull()
        )
        .dropDuplicates(
            ["event_id"]
        )
    )

    if event_type == "TransactionGenerator":

        df = df.filter(
            (col("amount") > 0)
            & col("transaction_type").isin(
                "PAYMENT",
                "TRANSFER",
                "WITHDRAWAL"
            )
            & (col("status") == "COMPLETED")
        )

    elif event_type == "AccountGenerator":

        df = df.filter(
            (col("balance") >= 0)
            & col("currency").isin(
                "PLN",
                "EUR",
                "USD"
            )
            & (col("status") == "ACTIVE")
        )

    elif event_type == "MerchantGenerator":

        df = df.filter(
            col("status") == "ACTIVE"
        )

    elif event_type == "CustomerGenerator":

        df = df.filter(
            col("risk_level").isin(
                "LOW",
                "MEDIUM",
                "HIGH"
            )
            & (col("status") == "ACTIVE")
        )

    else:
        raise ValueError(
            f"Unsupported event type: {event_type}"
        )

    return df