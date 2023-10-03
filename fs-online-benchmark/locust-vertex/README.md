
# Locust tests for Vertex FeatureStore

  

This runs locust tests for online read APIs for Vertex FS. It includes single and batch vector tests.

The google authentication and test parameters should be set in `vertex_configuration.json` first.

  

If the feature entity types are not already created, run `create_data.py` to ingest data from GCS source. Modify the config file accordingly.

The feature schema needs to be set in `features_schema.json` as this is required both while ingesting the data to FS and reading.

  

### Authentication to GCP

Authentication to GCP can be done by setting file path to user credentials application JSON or service account key file JSON. This is mainly required for distributed mode as it launches docker containers which will not have acces to your g. If you are not using distributed mode then your default `gcloud` user credentials will also work. Simply login to gcloud SDK `gcloud auth application-default login`. 

Typically a service account with access to feature store should be used by setting the account JSON key file path:
 
   1 . Create service account role with access to feature store e.g `Vertex AI Feature Store Admin`  
  2. Create and download JSON key
  3. Set the variable `GOOGLE_APPLICATION_CREDENTIALS`="path/to/key./json" in `vertex_configuration.json`. This will be set to create the environment variable while running the locust test.

  

### Steps to run  
#### Modify the vertex_configuration:
Set the Google Feature store project details. Also modify below fields accordingly:

- `gcs_source_uri` : This is optional and only used while creating data.

- `number_of_rows`: Total number of rows in data. Used while ramdomly sampling rows.

- `batch_size`: Size of the feature vectors to read for batch read.

- `GOOGLE_APPLICATION_CREDENTIALS` : Path to authentication key file JSON

- `feature_schema_json`: Path to JSON containing the schema of features

  ###

#### Single process

- Create a new conda environment
- Install the packages, `pip install -r requirements.txt`
- To run the tests from CLI, run command `locust --headless --users <NO_OF_USERS> --spawn-rate <NO_USERS_PER_SEC> -H https://{location}-aiplatform.googleapis.com --html result.html`

  

#### Distributed

- This is preferred for load testing with lot of users. Needs docker to be installed.

- Steps to install
	
  1.  `wget https://repo.hops.works/dev/dhananjay/vertex_locust.tar.gz`
  2.  `docker load < vertex_locust.tar.gz`

  

- Steps to run

 1. Modify the `docker-compose.yml` :

-  `-H` : hostname

-  `-u`: number of users

-  `-expect-workers`: number of workers

-  `-t`: test duration

-  `-r`: users spawn rate per second

2. By default the current directory is mounted to docker container. Modify the mounted directory to make it writable for all users as docker will write the result in this directory. Otherwise it may throw permission errors while writing the report file.

3. Run the tests by `sudo docker compose up --scale worker=<WORKER_COUNT>`
