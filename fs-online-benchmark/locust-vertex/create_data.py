from google.cloud import aiplatform
import json
from google.cloud.aiplatform import Feature, Featurestore
import random
import string
from datetime import datetime
import os
import google.auth

class CreateData:

    def __init__(self) -> None:

        # Set your project ID and location
        with open("vertex_configuration.json") as json_file:
            config_data = json.load(json_file)

        self.location = config_data.get("location")
        self.project_id = config_data.get("project")
        self.featurestore_id = config_data.get("feature_store")
        self.entity_type_id = config_data.get("entity_name")
        self.gcs_source_uri =  config_data.get("gcs_source_uri") # Replace with your GCS path
        self.primary_key = config_data.get("primary_key_id")

        self.creds,_ = google.auth.default();
        aiplatform.init(project=self.project_id, location=self.location, credentials=self.creds)
        # Step 1: Create an entity type in Google Feature Store
        self.featurestore = aiplatform.gapic.FeaturestoreServiceClient(client_options={"api_endpoint": f"{self.location}-aiplatform.googleapis.com"})
        self.entity_type_api = aiplatform.gapic.EntityType()
        self.fs =  Featurestore(
                featurestore_name=self.featurestore_id,
                project=self.project_id,
                location=self.location
            )

    def get_or_create_entity(self, entity_name):
        # Create the entity type
        try:
            entity_type = aiplatform.EntityType.create(
                entity_type_id=entity_name, featurestore_name=self.featurestore_id
            )
        except:
            print("Reading existing entity type")
            entity_type=self.fs.get_entity_type(entity_name)


        entity_type.wait()
        return  entity_type

    def create_features(self,entity_type):
        with open("features_schema.json") as f:
            FEATURE_CONFIGS = json.load(f)

        entity_type.batch_create_features(
            feature_configs=FEATURE_CONFIGS, sync=True)

    def ingest_data(self,entity_type, workers=1):
        # Step 3: Ingest data into the entity type using ingest_from_gcs
        entity_type.ingest_from_gcs(
            feature_ids= [feature.name for feature in entity_type.list_features()],
            feature_time=datetime.strptime('20/09/23',
                        '%d/%m/%y'),
            entity_id_field=self.primary_key,
            gcs_source_uris=self.gcs_source_uri,
            gcs_source_type="csv",
            worker_count=workers,
            sync=True,
        )


data = CreateData()

entity = data.get_or_create_entity("nyc_1ml_v3")
data.create_features(entity)
data.ingest_data(entity, workers=2)
