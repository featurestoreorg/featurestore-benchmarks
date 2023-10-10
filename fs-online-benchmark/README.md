# Feature Store Online Read Latency


In this benchmark, we measure the read **50, 90, 95, and 99 percential latencies** for reading from an online feature store, when reading individual feature vectors and batches of feature vectors.


## Benchmarked Feature Stores

The current feature stores benchmarked here are:

 * Hopsworks Feature Store, version 3.4
 * Vertex Feature Store (Legacy), version (September 2023)
 * Sagemaker Feature Store, version  (September 2023)

(We did not benchmark Databricks Feature Store, because Databricks Feature Store as of now does not have a public API for reading online table. Reading online data can instead be done by querying its underlyging online database provider e.g. AWS, Azure).

# How to run the Benchmarks

We use locust framework for load testing. The locustfiles can be launched on a client machine. It can launched either as a standlone process or in distributed mode using docker. Individual feature store specific instructions can be found under its sub-directory. For Hopsworks Featue Store we used locust framework as part of its feature store API [git repo](https://github.com/logicalclocks/feature-store-api/tree/master/locust_benchmark).

# Benchmarking setup
The client VMs used for running locusts are as shown here

<img src="./images/locust_vm.png" width="400" />

We run the test using the default settings and configuration available by each feature store. 

We ran the load tests with a throughput which was stable across all feature stores without causing excessive load on the client VMs.

#### Locust parameters
The locust framework was run in distributed mode using docker. Following parameters were used while running locust:

- Number of users=100
- Test duration=15 minutes
- Read request batch size= 1,100,250,500
- Locust workers=32
- Spawn rate=1



#### Data
 We used a small subset of NYC taxi data with 500 records. The data can be found [here](https://repo.hops.works/dev/davit/nyc_taxi/rides500.csv)

#### Batch size limits and soft quotas

Every feature store as a different limit/soft quotas on the maximum batch size for each read request. Particulary for this test the relevant are that Vertex and SageMaker have a default limit of **100** records for each request. 

The default maximum througput limit for SageMaker and Vertex Feature Store is 500 and 5000 requests/sec. We ran the tests below these thresholds.

More details about quotas and limits, for 
[SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-quotas.html) and [Vertex FeatureStore](https://cloud.google.com/vertex-ai/docs/quotas#featurestore).



# Benchmark Results

Following were the latencies as reported in locust results. 



- Latencies for batch size=1 (single feature vector)

<img src="./images/Batch_1.png" width="600" />

- Latencies for batch size=100

 <img src="./images/Batch_100.png" width="600" />

- Latencies for batch size=250*

 <img src="./images/Batch_250.png" width="600" />


- Latencies for batch size=500*

 <img src="./images/Batch_500.png" width="600" />

<br/><br/>


> *SageMaker and Vertex have a batch size limit of 100 records per request. Therefore for testing batch size 250 and 500 we ran sequentially a batch size of 100 for 3 and 5 times respectively.



