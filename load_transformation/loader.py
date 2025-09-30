import logging
from pyspark.sql.functions import col
from config.schemas import get_product_schema, get_orders_schema

logger = logging.getLogger(__name__)


def load_and_validate_data(spark, raw_order_path, raw_product_path):
    """
    Load and validate raw CSV data from file paths.

    Returns:
        tuple: (products_df, orders_df) - Validated DataFrames
    """
    product_schema = get_product_schema()
    orders_schema = get_orders_schema()
    try:
        logger.info("Loading data files")
        products_df = (
            spark.read.option("header", "true")
            .option("inferSchema", "false")
            .schema(product_schema)
            .csv(raw_product_path)
        )

        orders_df = (
            spark.read.option("header", "true")
            .option("inferSchema", "false")
            .schema(orders_schema)
            .csv(raw_order_path)
        )

        # Basic validation
        products_count = products_df.count()
        orders_count = orders_df.count()

        if products_count == 0 or orders_count == 0:
            raise ValueError("Empty datasets detected")

        logger.info(f"Loaded {products_count:,} products and {orders_count:,} orders")

        # Check for nulls in key columns
        products_nulls = products_df.filter(col("Product ID").isNull()).count()
        orders_nulls = orders_df.filter(col("Order ID").isNull()).count()

        if products_nulls > 0 or orders_nulls > 0:
            logger.warning(
                f"Found nulls - Products: {products_nulls}, Orders: {orders_nulls}"
            )

        return products_df, orders_df

    except Exception as e:
        logger.error(f"Data loading failed: {str(e)}")
