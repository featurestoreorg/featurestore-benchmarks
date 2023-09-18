# Feature Store Offline API Read Benchmarks

[ Diagram of the 3-phase Pipeline, highlighting what we are benchmarking]


## Benchmarked Feature Stores

The current feature stores benchmarked here are:

 * Hopsworks Feature Store, version 3.4
 * Vertex Feature Store, version X
 * Databricks Feature Store, version
 * Sagemaker Feature Store, version 

# How to run the Benchmarks

Run the notebooks included here in Hopsworks Jupyter, Databricks, Sagemaker Jupyterlab, Vertex Notebooks.


# Benchmark Setup

![experiment_setup_hardware](./images/fs-offline-experiment-setup-hardware.png)

Hardware setup for feature stores used in benchmarks

![experiment_setup_dataset](./images/fs-offline-read-dataset.png)

We use orginal data is NYC Taxi Trip data is available as files stored in the Parquet format, and is published monthly (with a 2 month delay).
Datasets used for offline read benchmarks

# Read Pandas DataFrame Benchmarks

![pandas_read_secs](./images/fs-offline-pandas-read-throughput-secs.png)


![pandas_read_relative](./images/fs-offline-pandas-read-throughput-relative.png)


# Create Parquet Training Data as Files Benchmark

![pandas_td_create_secs](./images/fs-offline-td-write-throughput-secs.png)


![pandas_td_create_secs](./images/fs-offline-td-write-throughput-relative.png)


# Pandas Point-in-Time Join Benchmark

![pit_join_secs](./images/fs-offline-pit-join-pandas-throughput-secs.png)


![pit_join_secs](./images/fs-offline-pit-join-pandas-throughput-relative.png)


# Create Parquet Training Data with Point-in-Time Join Benchmark

![pit_join_secs](./images/fs-offline-pit-join-td-throughput-secs.png)


![pit_join_secs](./images/fs-offline-pit-join-td-throughput-relative.png)

