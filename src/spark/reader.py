from pyspark.sql import DataFrame, SparkSession

from config.settings import KAFKA_BOOTSTRAP_SERVER, SPARK_BATCH_SIZE


def read_events(spark: SparkSession, topic: str) -> DataFrame:

    df = spark \
        .readStream.format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER) \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", SPARK_BATCH_SIZE) \
        .load() \

    return df