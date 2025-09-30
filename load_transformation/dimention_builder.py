from pyspark.sql.functions import col
from .utils import add_surrogate_key, add_audit_column


def build_product_dimension(products_df):
    """
    Build product dimension table with surrogate keys and audit columns.

    Returns:
        DataFrame: Product dimension with product_key, metadata
    """
    dim_product = products_df.select(
        col("Product ID").alias("product_id"),
        col("Product Name").alias("name"),
        col("Product Line").alias("line"),
        col("Product Category").alias("category"),
        col("Product Group").alias("group"),
    ).distinct()

    dim_product = add_surrogate_key(dim_product, "product_key", "product_id")
    dim_product = add_audit_column(dim_product)

    return dim_product


def build_supplier_dimension(products_df):
    """Build supplier dimension from product data."""
    dim_supplier = products_df.select(
        col("Supplier ID").alias("supplier_id"),
        col("Supplier Name").alias("name"),
        col("Supplier Country").alias("country"),
    ).distinct()

    dim_supplier = add_surrogate_key(dim_supplier, "supplier_key", "supplier_id")
    dim_supplier = add_audit_column(dim_supplier)

    return dim_supplier


def build_customer_dimension(orders_df):
    """Build customer dimension from order data."""
    dim_customer = orders_df.select(
        col("Customer ID").alias("customer_id"), col("Customer Status").alias("status")
    ).distinct()

    dim_customer = add_surrogate_key(dim_customer, "customer_key", "customer_id")
    dim_customer = add_audit_column(dim_customer)

    return dim_customer
