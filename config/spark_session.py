import os
from pyspark.sql import SparkSession


def create_spark_session():
    spark_memory = os.getenv("DRIVER_MEMORY", "4g")
    executor_memory = os.getenv("EXECUTOR_MEMORY", "2g")

    """Initialize Spark session with optimized configurations"""
    spark = (
        SparkSession.builder.appName("ETL_Pipeline_Prototype")
        .config("spark.driver.memory", spark_memory)
        .config("spark.executor.memory", executor_memory)
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )
    return spark
