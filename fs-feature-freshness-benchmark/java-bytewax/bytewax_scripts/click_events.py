import numpy as np

from datetime import datetime, timezone

from bytewax.dataflow import Dataflow
from bytewax.inputs import DynamicInput, PartitionedInput, StatefulSource, StatelessSource
from hsfs_bytewax_util import KafkaOutput, serialize_with_key

import hopsworks


class ClickEventSource(StatelessSource):
    def __init__(self):
        self._counter = 0

    def next_batch(self):
        self._counter += 1
        return [{
            "user_id": self._counter,
            "product_id": np.random.randint(low=0, high=1000),
            "timestamp": datetime.now(timezone.utc).now(timezone.utc),
            "clicks":  [np.random.randint(5) for _ in range(5)],
        }]


class ClickEventInput(DynamicInput):
    def __init__(self):
        pass

    def build(self, worker_index, worker_count):
        return ClickEventSource()


def key_on_product(data):
    return data["user_id"], data


def get_flow(feature_group_name, feature_group_version, hopsworks_host, hopsworks_project, hopsworks_api_key):
    flow = Dataflow()
    flow.input("input", ClickEventInput())
    flow.map(key_on_product)

    # get feature store handle
    project = hopsworks.login(
        host=hopsworks_host,
        project=hopsworks_project,
        api_key_value=hopsworks_api_key
    )

    fs = project.get_feature_store()

    # get feature group and its topic configuration
    feature_group = fs.get_feature_group(feature_group_name, feature_group_version)

    # sync to feature group topic
    flow.map(lambda x: serialize_with_key(x, feature_group))
    flow.output(
        "out",
        KafkaOutput(feature_group)
    )
    return flow