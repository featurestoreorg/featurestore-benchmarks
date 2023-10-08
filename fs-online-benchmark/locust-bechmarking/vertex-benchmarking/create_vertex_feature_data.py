from google.cloud import aiplatform
import json
from google.cloud.aiplatform import Feature, Featurestore
import random
import string
from datetime import datetime
import os
import google.auth

class VertexCreateEntityHelper:

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
        self.schema = config_data.get("feature_schema_json")
        if config_data.get("GOOGLE_APPLICATION_CREDENTIALS"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(config_data.pop("GOOGLE_APPLICATION_CREDENTIALS"))


        aiplatform.init(project=self.project_id, location=self.location)
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
        with open(self.schema) as f:
            FEATURE_CONFIGS = json.load(f)

        entity_type.batch_create_features(
            feature_configs=FEATURE_CONFIGS, sync=True)

    def ingest_data(self,entity_type, workers=1):
        # Step 3: Ingest data into the entity type using ingest_from_gcs
        entity_type.ingest_from_gcs(
            feature_ids= [feature.name for feature in entity_type.list_features()],
            feature_time= "timestamp", #datetime.strptime('06/10/23','%d/%m/%y'),#"eventtime",
            entity_id_field=self.primary_key,
            gcs_source_uris=self.gcs_source_uri,
            gcs_source_type="csv",
            worker_count=workers,
            sync=True,
        )


vertex_helper = VertexCreateEntityHelper()

entity = vertex_helper.get_or_create_entity(vertex_helper.entity_type_id)
vertex_helper.create_features(entity)
vertex_helper.ingest_data(entity, workers=2)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=""