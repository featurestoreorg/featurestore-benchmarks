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


![pandas_read_secs](./images/fs-offline-pandas-read-throughput-secs.png)
Read from Offline Feature Store to Pandas Throughput (time taken)

![pandas_read_relative](./images/fs-offline-pandas-read-throughput-relative.png)
Read from Offline Feature Store to Pandas Throughput (relative)t
