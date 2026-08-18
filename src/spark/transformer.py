from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    from_json,
    to_timestamp,
)
from pyspark.sql.types import StructType

TABLE_COLUMNS = {
    "customers": {
        "date_column": "registration_date",
        "columns": [
            "customer_id", "first_name", "last_name",
            "country", "city", "risk_level", "status",
        ],
        "renames": {},
    },
    "accounts": {
        "date_column": "created_at",
        "columns": [
            "account_id", "customer_id", "iban",
            "currency", "balance", "status",
        ],
        "renames": {},
    },
    "merchants": {
        "date_column": None,
        "columns": ["merchant_id", "name", "category", "country", "risk_level"],
        "renames": {"merchant_name": "name"},
    },
    "transactions": {
        "date_column": "transaction_date",
        "columns": [
            "transaction_id", "account_id", "merchant_id",
            "amount", "currency", "status",
        ],
        "renames": {},
    },
}


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


def project_for_table(
    df: DataFrame,
    table_name: str
) -> DataFrame:

    config = TABLE_COLUMNS[table_name]

    for old_name, new_name in config["renames"].items():
        df = df.withColumnRenamed(old_name, new_name)

    columns = config["columns"]
    if config["date_column"]:
        df = df.withColumnRenamed("timestamp", config["date_column"])
        columns = [*columns, config["date_column"]]

    return df.select(*columns)