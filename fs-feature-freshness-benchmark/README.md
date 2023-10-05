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

## Setup
Install the required python libraries
```console
pip install hopsworks
pip install bytewax
```

## Clone tutorials repository
```bash
git clone https://github.com/featurestoreorg/featurestore-benchmarks
cd ./featurestore-benchmarks/fs-feature-freshness-benchmark/java-bytewax
```

## Build the Java client
```console
mvn clean compile assembly:single
# Jar will be created as target/bytewaxlatencybenchmark-1.0-SNAPSHOT-jar-with-dependencies.jar
```

## Define environment variables
You need  to have Hopsworks cluster host address, hopsworks project name and
[api key](https://docs.hopsworks.ai/3.3/user_guides/projects/api_key/create_api_key/)

Once you have the above, define the following environment variables:

**Console 1: Define variables**
```console
export FEATURE_GROUP_NAME=clicks
export FEATURE_GROUP_VERSION=1
export HOPSWORKS_HOST=REPLACE_WITH_YOUR_HOPSWOKRKS_CLUSTER_HOST
export HOPSWORKS_API_KEY=REPLACE_WITH_YOUR_HOPSWORKS_API_KEY
export HOPSWOERKS_PROJECT_NAME=REPLACE_WITH_YOUR_HOPSWOERKS_PROJECT_NAME
```

## Create a feature group using the HSFS APIs.
Full documentation how to create feature group using HSFS APIs can be found [here](https://docs.hopsworks.ai/3.3/user_guides/fs/feature_group/create/).

**Console 1: Create the feature group**
```console
python3 ./bytewax_scripts/recreate_fg.py
```

## Start the benchmarking tool
**Console 2: Start the benchmarking tool**
To get necessary environment variables in Feature Store UI go to Storage Connectors -> 
FEATURE_STORENAME_USER_onlinefeaturestore. Then click to edit button and Select following variables:
```console
export DB_URL="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_URL" # You might need to change the IP to an IP that you can reach from your benchmark machine
export USER="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_USER"
export PASS="REPLACE_WITH_YOUR_ONLINE_FEATURE_STORE_CONNECTOR_PASSWORD"

java -jar bytewaxlatencybenchmark-1.0-SNAPSHOT-jar-with-dependencies.jar BATCH_SIZE START_ID ROUNDS
# BATCH_SIZE - Maximum number of ids to be fetched in one request. Default is 50.
# START_ID - Id of the first record to be fetched. Default is 1.
# ROUNDS - How many batches to fetch. Default is 100.
```

## Simulate click events and write to online feature store.
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

# Benchmark Results


