from pyspark.sql.functions import col, to_date, round
from .utils import add_surrogate_key, add_audit_column


def build_fact_orders(orders_df, dim_product, dim_supplier, dim_customer, products_df):
    """
    Build fact table by joining orders with dimension tables.

    Returns:
        DataFrame: Fact table with surrogate keys and calculated measures
    """
    # Prepare orders data with date conversions
    fact_prep = orders_df.select(
        col("Order ID").alias("order_id"),
        col("Product ID").alias("product_id"),
        col("Customer ID").alias("customer_id"),
        to_date(col("Date Order was placed"), "dd-MMM-yy").alias("order_date"),
        to_date(col("Delivery Date"), "dd-MMM-yy").alias("delivery_date"),
        col("Quantity Ordered").alias("order_quantity"),
        col("Total Retail Price for This Order").alias("total_retail_price"),
        col("Cost Price Per Unit").alias("unit_price"),
    )

    # Join with product dimension to get product_key
    fact_with_product = fact_prep.join(
        dim_product.select("product_key", "product_id"), "product_id", "inner"
    )

    # Join with supplier through products data
    product_supplier = products_df.select(
        col("Product ID").alias("product_id"), col("Supplier ID").alias("supplier_id")
    ).distinct()

    fact_with_supplier = fact_with_product.join(
        product_supplier, "product_id", "inner"
    ).join(dim_supplier.select("supplier_key", "supplier_id"), "supplier_id", "inner")

    # Join with customer dimension
    fact_orders = fact_with_supplier.join(
        dim_customer.select("customer_key", "customer_id"), "customer_id", "inner"
    )

    fact_orders = fact_orders.select(
        col("order_id"),
        col("product_key"),
        col("supplier_key"),
        col("customer_key"),
        col("order_date"),
        col("delivery_date"),
        col("order_quantity"),
        col("unit_price"),
        col("total_retail_price"),
        (col("order_quantity") * col("unit_price")).alias("total_cost"),
        round(
            col("total_retail_price") - (col("order_quantity") * col("unit_price")), 2
        ).alias("gross_profit"),
    )

    orderby_keys = ["order_id", "product_key"]
    fact_orders = add_surrogate_key(fact_orders, "order_key", orderby_keys)
    fact_orders = add_audit_column(fact_orders)

    return fact_orders
