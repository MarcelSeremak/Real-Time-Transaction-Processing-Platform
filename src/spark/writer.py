from pyspark.sql import DataFrame

from config.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from utils.logger import get_logger

logger = get_logger("SPARK_WRITER")

FK_DEPENDENCIES = {
    "accounts": [("customer_id", "customers", "customer_id")],
    "transactions": [
        ("account_id", "accounts", "account_id"),
        ("merchant_id", "merchants", "merchant_id"),
    ],
}


def _jdbc_url() -> str:
    return f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def _read_table(spark, table_name: str) -> DataFrame:
    return (
        spark.read
        .format("jdbc")
        .option("url", _jdbc_url())
        .option("dbtable", table_name)
        .option("user", POSTGRES_USER)
        .option("password", POSTGRES_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .load()
    )


def drop_orphan_rows(df: DataFrame, table_name: str) -> DataFrame:
    """Drop rows whose FK reference isn't committed in Postgres yet.

    The Kafka producers pick "existing" parent ids straight from Redis,
    which is updated synchronously and can be ahead of what this same
    micro-batch's siblings have actually flushed to Postgres. Without this
    filter, one such row aborts the whole JDBC batch insert and kills the
    streaming query.
    """

    for local_col, parent_table, parent_col in FK_DEPENDENCIES.get(table_name, []):
        parent_ids = (
            _read_table(df.sparkSession, parent_table)
            .select(parent_col)
            .distinct()
        )
        before = df.count()
        df = df.join(
            parent_ids,
            df[local_col] == parent_ids[parent_col],
            "left_semi"
        )
        dropped = before - df.count()
        if dropped:
            logger.warning(
                f"Dropped {dropped} row(s) from {table_name}: "
                f"{local_col} not yet present in {parent_table}"
            )

    return df


def write_to_postgres(
    df: DataFrame,
    table_name: str,
) -> None:

    df = drop_orphan_rows(df, table_name)

    (
        df.write
        .format("jdbc")
        .option("url", _jdbc_url())
        .option("dbtable", table_name)
        .option("user", POSTGRES_USER)
        .option("password", POSTGRES_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .option("stringtype", "unspecified")
        .mode("append")
        .save()
    )
