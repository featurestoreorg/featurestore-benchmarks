# Feature Store Freshness Benchmarks


In this benchmark, we measure the best-case, average-case, and worst-case performance of feature stores in going from 
raw event data in a message bus (Kafka, Polars, etc) to a stream processing feature pipeline computing (or recomputing) 
the updated or new feature value, and then writing that feature value to the online feature store. That is, the time 
stops when the computed feature becomes available in the online feature store for reading.

- [java-bytewax](https://github.com/featurestoreorg/featurestore-benchmarks/tree/main/fs-feature-freshness-benchmark/java-bytewax):
Feature Store Freshness using Bytewax event simulator and java application for fetching feature vectors


## Benchmarked Feature Stores

The current feature stores benchmarked here are:

 * Hopsworks Feature Store

# How to run the Benchmarks

Run the notebooks included here in Hopsworks Jupyter, Databricks, Sagemaker Jupyterlab, Vertex Notebooks.

# Benchmark Results


