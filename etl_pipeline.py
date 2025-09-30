"""
ETL Pipeline for Data Warehouse
Processes product and order data into dimensional model with fact and dimension tables.
"""
import os
import logging
import sys

from config.spark_session import create_spark_session
from dotenv import load_dotenv
from load_transformation.dimention_builder import (
    build_customer_dimension,
    build_product_dimension,
    build_supplier_dimension,
)
from load_transformation.fact_builder import build_fact_orders
from load_transformation.loader import load_and_validate_data
from load_transformation.writer import write_to_parquet

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main ETL pipeline execution."""
    logger.info("Starting ETL Pipeline")

    try:
        # Initialize environment and Spark session
        load_dotenv()
        spark = create_spark_session()

        # Get file paths from environment
        raw_order_path = os.getenv("RAW_ORDER_TABLE_PATH")
        raw_product_path = os.getenv("RAW_PRODUCT_TABLE_PATH")

        dim_product_path = os.getenv("OUTPUT_DIM_PRODUCT")
        dim_supplier_path = os.getenv("OUTPUT_DIM_SUPPLIER")
        dim_customer_path = os.getenv("OUTPUT_DIM_CUSTOMER")
        fact_orders_path = os.getenv("OUTPUT_FACT_ORDERS")

        # Extract and validate raw data
        products_df, orders_df = load_and_validate_data(
            spark, raw_order_path, raw_product_path
        )

        # Transform: Build dimension tables
        dim_product = build_product_dimension(products_df)
        dim_supplier = build_supplier_dimension(products_df)
        dim_customer = build_customer_dimension(orders_df)

        logger.info(
            f"Dimensions created - Products: {dim_product.count():,}, Suppliers: {dim_supplier.count():,}, Customers: {dim_customer.count():,}"
        )

        # Transform: Build fact table
        fact_orders = build_fact_orders(
            orders_df, dim_product, dim_supplier, dim_customer, products_df
        )

        logger.info(f"Fact table created with {fact_orders.count():,} orders")

        # Load: Write all tables to Parquet format
        write_to_parquet(
            dim_product,
            dim_product_path,
            dim_supplier,
            dim_supplier_path,
            dim_customer,
            dim_customer_path,
            fact_orders,
            fact_orders_path,
        )

        logger.info("ETL Pipeline completed successfully")
        print("ETL Pipeline completed successfully!")

    except Exception as e:
        logger.error(f"ETL Pipeline failed: {str(e)}")
        print(f"ETL Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
