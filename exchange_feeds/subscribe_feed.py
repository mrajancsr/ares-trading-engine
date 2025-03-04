# -- To run the file, go to shell and type:
# -- python3 feed_ingestor_to_redis.py -t 'ethusdt' -n 'binance-blotter'
# -- To save the stream, type
# -- python3 feed_ingestor_to_redis.py -t 'ETH/USDT' -n 'kraken-L1' -s 'yes'

import argparse
import asyncio

import uvloop

from binance import BinanceBlotter, BinanceOrderBook
from constants import STREAM_NAMES
from kraken import KrakenBlotter, KrakenOrderBook

# event policy needs to be set at top of file
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

factory = {}
factory["binance-blotter"] = BinanceBlotter
factory["kraken-orderbook"] = KrakenOrderBook
factory["kraken-blotter"] = KrakenBlotter
factory["binance-L1"] = BinanceOrderBook


async def subscribe_to_exchange():
    parser = argparse.ArgumentParser(
        prog="subscribe_feed",
        usage="%(prog)s --symbol [options] --stream_name [options]",
        description="Streams Raw Feeds from Exchange",
        epilog="sit back and drink coffee - long running program",
    )
    parser.add_argument(
        "--ticker",
        "-t",
        action="store",
        required=True,
        type=str,
        help="ticker symbol from exchange",
    )
    parser.add_argument(
        "--stream_name",
        "-n",
        action="store",
        required=True,
        type=str,
        help="stream name in redis to store data to",
        choices=STREAM_NAMES,
    )
    parser.add_argument(
        "--save_stream",
        "-s",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="to save to redis",
    )
    args = parser.parse_args()

    ticker, stream_name, save_stream = args.ticker, args.stream_name, args.save_stream
    if stream_name not in factory:
        raise KeyError("stream name not found")

    exchange = factory[stream_name]
    async with exchange(ticker, stream_name) as exchg:
        print(
            f"Connecting to {exchg.exchange}.  If an error occurs please press ctrl + c to stop this forever process"
        )
        print("erorrs are logged at exchange_feeds/exchangelogs.log")
        await exchg.stream(save_stream=save_stream)


if __name__ == "__main__":
    asyncio.run(subscribe_to_exchange())
