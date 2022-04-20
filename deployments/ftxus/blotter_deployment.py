import os
from os.path import join

import ccxt

from exchange_feeds.constants import EXCHANGEPATH, PHOBOSPATH
from prefect.deployments import DeploymentSpec
from deployments.exchange_markets.markets import get_market_symbols
from exchange_feeds.constants import StreamName


path_to_pipeline = join(PHOBOSPATH, "pipelines", "feed_to_redis_pipeline.py")
path_to_file = os.path.join(EXCHANGEPATH, "feed_ingestor_to_redis.py")

stream_name = StreamName.FTXUS_BLOTTER.value
spec_name_prefix = stream_name.replace("-", "_")
for symbol in get_market_symbols(ccxt.ftxus()):
    tag = symbol.replace("/", "").lower()
    DeploymentSpec(
        name=f"{spec_name_prefix}_{tag}",
        flow_location=path_to_pipeline,
        tags=[stream_name, tag],
        parameters={
            "shell_task": path_to_file,
            "symbol": symbol,
            "stream_name": stream_name,
        },
    )
