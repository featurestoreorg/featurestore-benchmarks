import random
from time import sleep
from locust import FastHttpUser, HttpUser, User, constant, task, between, events, constant_throughput
from locust.runners import MasterRunner

import json
import google.auth
import google.auth.transport.requests
import numpy as np
import os
from common.stop_watch import stopwatch

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    environment.work_dir = "./"
    if isinstance(environment.runner, MasterRunner):
        print("Running on master node, distributed mode")
        environment.work_dir = "/home/locust"
        print("Setting parent directory for configurations files:", environment.work_dir)
    else:
        print("Running on a worker or standalone mode")        
        print("Using parent directory for configurations files:", environment.work_dir)

    with open(os.path.join(environment.work_dir,"vertex_configuration.json")) as json_file:
        config_data = json.load(json_file)          

    environment.location = config_data.get("location")
    environment.project = config_data.get("project")
    environment.feature_store = config_data.get("feature_store")
    environment.number_of_rows= config_data.get("number_of_rows")
    environment.entity_name = config_data.get("entity_name")
    environment.batch_size = config_data.get("batch_size")
    environment.schema_json = config_data.get("feature_schema_json")
    if config_data.get("GOOGLE_APPLICATION_CREDENTIALS"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(environment.work_dir, config_data.pop("GOOGLE_APPLICATION_CREDENTIALS"))



@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("A new test is starting")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("A new test is ending")


class VertexTestOnlineRead(FastHttpUser):
    wait_time = constant(0.1)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
       

    def on_start(self):
         # authenticate
        creds, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        creds.refresh(google.auth.transport.requests.Request())
        self.client.headers = {"Authorization": f"Bearer {creds.token}","Connection": "keep-alive","Keep-Alive": "timeout=5, max=2000"}
        self.wait()
    
    @task
    def read_online_single_all_features(self):
        # online read feature vector- all columns single row  

        # read json schema      
        with open(os.path.join(self.environment.work_dir, self.environment.schema_json)) as f:
            schema = json.load(f)
        # payload
        data = {
            "entityId": str(np.random.randint(self.environment.number_of_rows)),
            "featureSelector": {
                "idMatcher": {
                    "ids": list(schema)
                }
            }
        }
        # send
        self.client.post(
            url=f"/v1/projects/{self.environment.project}/locations/{self.environment.location}/featurestores/{self.environment.feature_store}/entityTypes/{self.environment.entity_name}:readFeatureValues",
            json=data,
             headers=self.client.headers
            
        )
        

    @task
    def read_online_single_feature(self):
        # online read feature vector- single random column single row
        
        # read json schema
        with open(os.path.join(self.environment.work_dir, self.environment.schema_json)) as f:
            schema = json.load(f)

        feature_ids = list(schema)
        # payload
        data = {
            "entityId": str(np.random.randint(self.environment.number_of_rows)),
            "featureSelector": {
                "idMatcher": {
                    "ids": random.choice(feature_ids)
                }
            }
        }
        # send 
        response = self.client.post(
            url=f"/v1/projects/{self.environment.project}/locations/{self.environment.location}/featurestores/{self.environment.feature_store}/entityTypes/{self.environment.entity_name}:readFeatureValues",
            json=data,
            headers=self.client.headers
        )

    @task
    def read_online_batch_features(self):
        # online read feature vector      

        # read json schema  
        with open(os.path.join(self.environment.work_dir, self.environment.schema_json)) as f:
            schema = json.load(f)
        # payload
        data = {
            "entityIds": [str(random.randint(0, self.environment.number_of_rows-1)) for i in range(self.environment.batch_size)],
            "featureSelector": {
                "idMatcher": {
                    "ids": list(schema)
                }
            }
        }
         # send 
        self.client.post(
            url=f"/v1/projects/{self.environment.project}/locations/{self.environment.location}/featurestores/{self.environment.feature_store}/entityTypes/{self.environment.entity_name}:streamingReadFeatureValues",
            json=data,
            headers=self.client.headers
        )