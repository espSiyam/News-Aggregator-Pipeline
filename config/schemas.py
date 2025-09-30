from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
)


def get_product_schema():
    """Define schema for product-supplier data"""
    return StructType(
        [
            StructField("Product ID", StringType(), False),
            StructField("Product Line", StringType(), False),
            StructField("Product Category", StringType(), False),
            StructField("Product Group", StringType(), False),
            StructField("Product Name", StringType(), False),
            StructField("Supplier Country", StringType(), False),
            StructField("Supplier Name", StringType(), False),
            StructField("Supplier ID", StringType(), False),
        ]
    )


def get_orders_schema():
    """Define schema for orders data"""
    return StructType(
        [
            StructField("Customer ID", StringType(), False),
            StructField("Customer Status", StringType(), False),
            StructField("Date Order was placed", StringType(), False),
            StructField("Delivery Date", StringType(), False),
            StructField("Order ID", StringType(), False),
            StructField("Product ID", StringType(), False),
            StructField("Quantity Ordered", IntegerType(), False),
            StructField("Total Retail Price for This Order", DoubleType(), False),
            StructField("Cost Price Per Unit", DoubleType(), False),
        ]
    )
