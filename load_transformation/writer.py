import os
import logging
from pyspark.sql.functions import year, month

logger = logging.getLogger(__name__)


def write_to_parquet(
    dim_product,
    dim_product_path,
    dim_supplier,
    dim_supplier_path,
    dim_customer,
    dim_customer_path,
    fact_orders,
    fact_orders_path,
):
    """
    Write all dimension and fact tables to Parquet format with compression.
    Fact table is partitioned by year/month for query performance.
    """
    try:
        logger.info("Writing tables to Parquet format")

        # Write dimension tables
        dim_product.coalesce(1).write.mode("overwrite").option(
            "compression", "snappy"
        ).parquet(dim_product_path)

        dim_supplier.coalesce(1).write.mode("overwrite").option(
            "compression", "snappy"
        ).parquet(dim_supplier_path)

        dim_customer.coalesce(1).write.mode("overwrite").option(
            "compression", "snappy"
        ).parquet(dim_customer_path)

        # Write fact table with date partitioning
        (
            fact_orders.withColumn("year", year("order_date"))
            .withColumn("month", month("order_date"))
            .write.mode("overwrite")
            .option("compression", "snappy")
            .partitionBy("year", "month")
            .parquet(fact_orders_path)
        )

        logger.info("All tables written successfully")

    except Exception as e:
        logger.error(f"Failed to write Parquet files: {str(e)}")
        raise
