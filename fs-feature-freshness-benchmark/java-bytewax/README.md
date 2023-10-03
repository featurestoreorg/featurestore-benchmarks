# Feature Freshness Benchmarks

This benchmark measures feature freshness, which is the latency between events being created in 
the application (in this case Bytewax) and them being consumed from the online feature store by another application 
(in this case simple Java client).

## Setup
Install python libraries 
```console
pip install hopsworks
pip install bytewax
```

## BUILD java client
```console
mvn clean compile assembly:single
# Jar will be created as target/QueryBenchmark-1.0-SNAPSHOT-jar-with-dependencies.jar
```

## RUN
**Console 1: Create the feature group**
```console
export FEATURE_GROUP_NAME=clicks
export FEATURE_GROUP_VERSION=1
export HOPSWORKS_HOST=6d71e8e0-5b7f-11ee-9a46-03cec0f3024e.cloud.hopsworks.ai
export HOPSWORKS_API_KEY=REPLACE_WITH_YOUR_HOPSWORKS_API_KEY
export HOPSWOERKS_PROJECT_NAME=REPLACE_WITH_YOUR_HOPSWOERKS_PROJECT_NAME

python3 ./bytewax_scripts/recreate_fg.py
```
**Console 2: Start the benchmarking tool**
To get necessary environment variables in Feature Store UI go to Storage Connectors -> 
FEATURE_STORENAME_USER_onlinefeaturestore. Then click to edit button and Select following variables:
```console
export DB_URL="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_URL" # You might need to change the IP to an IP that you can reach from your benchmark machine
export USER="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_USER"
export PASS="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_PASSWORD"

java -cp QueryBenchmark-1.0-SNAPSHOT-jar-with-dependencies.jar org.example.BytewaxLatencyBenchmark BATCH_SIZE START_ID ROUNDS
# BATCH_SIZE - Maximum number of ids to be fetched in one request. Default is 50.
# START_ID - Id of the first record to be fetched. Default is 1.
# ROUNDS - How many batches to fetch. Default is 100.
```

**Console 1: Start sending records**
```console
cd bytewax_scripts
export HOPSWORKS_HOST=REPLACE_WITH_YOUR_HOPSWOKRKS_CLUSTER_HOST
export HOPSWORKS_API_KEY=REPLACE_WITH_YOUR_HOPSWORKS_API_KEY
export HOPSWOERKS_PROJECT_NAME=REPLACE_WITH_YOUR_HOPSWOERKS_PROJECT_NAME
export FEATURE_GROUP_NAME=clicks
export FEATURE_GROUP_VERSION=1

python3 -m bytewax.run "click_events:get_flow('$FEATURE_GROUP_NAME', $FEATURE_GROUP_VERSION, '$HOPSWORKS_HOST', '$HOPSWOERKS_PROJECT_NAME', '$HOPSWORKS_API_KEY')"
```

## Benchmark Results

**Measured latencies are for us-west-3a to us-west2-a:**

```console
java -cp QueryBenchmark-1.0-SNAPSHOT-jar-with-dependencies.jar org.example.BytewaxLatencyBenchmarkHopsworks 50 1 100
...
Statistics for 100 rounds with batches of size up to 50:

Minimum latency: 103ms
Maximum latency: 894ms
Average latency: 485ms

p50 latency: 483.5ms
p90 latency: 830.3ms
p95 latency: 849.3ms
p99 latency: 890.04ms
```
