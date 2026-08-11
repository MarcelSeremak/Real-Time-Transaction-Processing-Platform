from pyspark.sql.types import DoubleType, StringType, StructField, StructType

transaction_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("event_type", StringType(), False),
    StructField("timestamp", StringType(), False),
    StructField("data", StructType([
        StructField("transaction_id", StringType(), False),
        StructField("account_id", StringType(), False),
        StructField("merchant_id", StringType(), False),
        StructField("amount", DoubleType(), False),
        StructField("currency", StringType(), False),
        StructField("transaction_type", StringType(), False),
        StructField("status", StringType(), False),
    ]), False)
])



customer_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("event_type", StringType(), False),
    StructField("timestamp", StringType(), False),
    StructField("data", StructType([
        StructField("customer_id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("country", StringType(), False),
        StructField("city", StringType(), False),
        StructField("risk_level", StringType(), False),
        StructField("status", StringType(), False),
    ]), False),
])


merchant_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("event_type", StringType(), False),
    StructField("timestamp", StringType(), False),
    StructField("data", StructType([
        StructField("merchant_id", StringType(), False),
        StructField("merchant_name", StringType(), False),
        StructField("category", StringType(), False),
        StructField("country", StringType(), False),
        StructField("city", StringType(), False),
        StructField("status", StringType(), False),
    ]), False),
])


account_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("event_type", StringType(), False),
    StructField("timestamp", StringType(), False),
    StructField("data", StructType([
        StructField("account_id", StringType(), False),
        StructField("customer_id", StringType(), False),
        StructField("iban", StringType(), False),
        StructField("currency", StringType(), False),
        StructField("balance", DoubleType(), False),
        StructField("status", StringType(), False),
    ]), False),
])


