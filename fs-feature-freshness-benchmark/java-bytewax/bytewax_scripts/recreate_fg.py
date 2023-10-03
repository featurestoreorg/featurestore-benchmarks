import hopsworks

from hsfs.feature import Feature

project = hopsworks.login()
fs = project.get_feature_store()

try:
    fg = fs.get_feature_group(
        name="clicks",
        version=1)
    fg.delete()
except:
    pass

features = [
    Feature(name="user_id", type="bigint"),
    Feature(name="product_id", type="bigint"),
    Feature(name="timestamp", type="timestamp"),
    Feature(name="clicks", type="array<float>")
]

fg = fs.get_or_create_feature_group(
    name="clicks",
    version=1,
    primary_key=["user_id"],
    event_time="timestamp",
    statistics_config=False,
    online_enabled=True,
)

fg.save(features)
