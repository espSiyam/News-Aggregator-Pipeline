from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, current_timestamp, struct


def add_surrogate_key(dataframe, output_key, primary_keys):
    """Add auto-incrementing surrogate key to dimension tables."""

    if isinstance(primary_keys, (list, tuple)):
        window_spec = Window.orderBy(*primary_keys)
    else:
        window_spec = Window.orderBy(primary_keys)

    dataframe = dataframe.withColumn(output_key, row_number().over(window_spec))

    return dataframe


def add_audit_column(dataframe):
    """Add audit metadata with created_on/updated_on timestamps for SCD tracking."""
    dataframe = dataframe.withColumn(
        "metadata",
        struct(
            current_timestamp().alias("created_on"),
            current_timestamp().alias("updated_on"),
        ),
    )
    return dataframe
