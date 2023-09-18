# Feature Store Offline API Read Benchmarks

[ Diagram of the 3-phase Pipeline, highlighting what we are benchmarking]

## NYC Taxi Dataset 

The orginal data is NYC Taxi Trip data is available as files stored in the Parquet format, and is published monthly (with a 2 month delay).

## Read Pandas DataFrame Benchmark

## Create Training Data as Files Benchmark


## Point-in-Time Join Benchmark

## Benchmarked Feature Stores

The current feature stores benchmarked here are:

 * Hopsworks Feature Store
 * Vertex Feature Store
 * Databricks Feature Store
 * Sagemaker Feature Store

# How to run the Benchmarks

Run the notebooks included here in Hopsworks Jupyter, Databricks, Sagemaker Jupyterlab, Vertex Notebooks.

# Benchmark Results

![experiment_setup_hardware](./images/fs-offline-experiment-setup-hardware.png)

Hardware setup for feature stores used in benchmarks

![experiment_setup_dataset](./images/fs-offline-read-dataset.png)

Datasets used for offline read benchmarks


![pandas_read_secs](./images/fs-offline-pandas-read-throughput-secs.png)

Read from Offline Feature Store to Pandas Throughput (time taken)

![pandas_read_relative](./images/fs-offline-pandas-read-throughput-relative.png)

Read from Offline Feature Store to Pandas Throughput (relative)t


![pandas_td_create_secs](./images/fs-offline-td-write-throughput-secs.png)

Create Training Data as files using Offline Feature Store (time taken)

![pandas_td_create_secs](./images/fs-offline-td-write-throughput-relative.png)

Create Training Data as files using Offline Feature Store (relative)

![pit_join_secs](./images/fs-offline-pit-join-td-throughput-secs.png)

Point-in-Time Join (time taken)

![pit_join_secs](./images/fs-offline-pit-join-td-throughput-relative.png)

Point-in-Time Join (relative))

