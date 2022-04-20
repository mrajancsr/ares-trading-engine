import os
from os.path import join

from exchange_feeds.constants import EXCHANGEPATH, PHOBOSPATH
from prefect.deployments import DeploymentSpec

path_to_pipeline = join(PHOBOSPATH, "pipelines", "feed_to_redis_pipeline.py")
path_to_file = os.path.join(EXCHANGEPATH, "feed_ingestor_to_redis.py")


DeploymentSpec(
    name="binance_blotter_ethusdt",
    flow_location=path_to_pipeline,
    tags=["binance-blotter", "ethusdt"],
    parameters={
        "shell_task": path_to_file,
        "symbol": "ethusdt",
        "stream_name": "binance-blotter",
    },
)

DeploymentSpec(
    name="binance-blotter_btcusdt",
    flow_location=path_to_pipeline,
    tags=["binance-blotter", "btcusdt"],
    parameters={
        "shell_task": path_to_file,
        "symbol": "btcusdt",
        "stream_name": "binance-blotter",
    },
)
