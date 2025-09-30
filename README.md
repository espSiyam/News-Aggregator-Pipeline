# PySpark ETL Pipeline

Simple ETL pipeline to convert product and order CSV data into dimension and fact tables using PySpark.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Put your CSV files in `dataset/inputs/`:
   - `orders.csv` 
   - `product-supplier.csv`

3. Run the pipeline:
```bash
python elt_pipeline.py
```

## What the code does

1. **Extract**: Loads CSV files with predefined schemas
2. **Transform**: Creates dimension tables and joins them to build fact table
3. **Load**: Saves everything as compressed Parquet files

The fact table includes calculated fields like gross profit and is partitioned by date for better performance.