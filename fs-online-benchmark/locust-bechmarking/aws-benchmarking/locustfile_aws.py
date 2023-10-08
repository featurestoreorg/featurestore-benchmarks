import random
from locust import User, constant, task, events, run_single_user
from locust.runners import MasterRunner
import json
import numpy as np
import os
from common.stop_watch import stopwatch
import boto3
from botocore.config import Config


@events.init.add_listener
def on_locust_init(environment,**kwargs):
    environment.work_dir = ""
    LOCUST_WORK_DIR = "/home/locust"
    if isinstance(environment.runner, MasterRunner):
        print("Running on master node, distributed mode")
        environment.work_dir = LOCUST_WORK_DIR
        print("Setting parent directory for configurations files:", environment.work_dir)
    else:
        print("Running on a worker or standalone mode")     
    
    with open(os.path.join(environment.work_dir, os.path.join(environment.work_dir, "aws_configuration.json"))) as json_file:
        config_data = json.load(json_file)   
        
    environment.region = config_data.get("REGION")
    environment.fg_name = config_data.get("feature_group_name")
    environment.batch_size = config_data.get("batch_size")
    environment.number_of_rows = config_data.get("number_of_rows")
    environment.feature_names = config_data.get("feature_names")
    
    environment.boto_session =   boto3.Session(
        aws_access_key_id=config_data.get("AWS_ACCESS_KEY"), 
        aws_secret_access_key=config_data.get("AWS_SECRET"),
        region_name= environment.region
        )
    
    environment.featurestore_runtime = environment.boto_session.client(
        service_name="sagemaker-featurestore-runtime",
        region_name=environment.region,
        config=Config(retries={'max_attempts':10}, max_pool_connections=25)
        )  


class SagemakerOnlineRead(User):
    wait_time = constant(0.1)
    
    @events.init.add_listener
    def on_locust_init(environment,  **kwargs):
        print("Initiliasing test")        
   
    @task
    def test_single_vector(user):  
        user.single_read(fg_name=user.environment.fg_name, 
                         record_identifier_value= str(np.random.randint(user.environment.number_of_rows - 1))
                         )       
        return
    
    @task
    def test_batch_vector(user):        
        user.batch_read(fg_name=user.environment.fg_name, 
                        feature_ids = [str(random.randint(0, user.environment.number_of_rows -1)) for i in range(user.environment.batch_size)]  
                        )        
        return
    
    
    def test_single_vector_single_feature(user):
        if user.environment.feature_names:                     
            user.single_read_single_vector(
                fg_name=user.environment.fg_name, 
                record_identifier_value= str(np.random.randint(user.environment.number_of_rows - 1)), 
                features_names= user.environment.feature_names 
                )            
    
    @stopwatch
    def batch_read(user,fg_name, feature_ids):
        user.environment.featurestore_runtime.batch_get_record(
            Identifiers=[{
                "FeatureGroupName": fg_name,
                "RecordIdentifiersValueAsString":feature_ids,
                }]
            )
    
    @stopwatch    
    def single_read(user,  fg_name, record_identifier_value):        
        user.environment.featurestore_runtime.get_record(
            FeatureGroupName=fg_name,
            RecordIdentifierValueAsString=record_identifier_value
            )
        
    @stopwatch    
    def single_read_single_vector(user,  fg_name, record_identifier_value, features_names):            
        user.environment.featurestore_runtime.get_record(
            FeatureGroupName=fg_name,
            RecordIdentifierValueAsString=record_identifier_value,
            FeatureNames = features_names
            )

    
# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(SagemakerOnlineRead)