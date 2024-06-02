import asyncio
from datetime import datetime
from typing import List

import aiohttp
import pandas as pd
import pyarrow as pa

# from google.cloud import storage
import pytz
from pandas import Timestamp
from finclaw.utils.progress_bar import progress_bar

from finclaw.config import logger
from finclaw.data_store.schema import STOCK_SYMBOL
from finclaw.vendor.finnhub.finnhub_client import get_company_profile, get_stock_candle
from finclaw.vendor.finnhub.models import to_company_description_table, to_ohcl_table
from finclaw.vendor.finnhub.symbols import get_symbols_for

# storage_client = storage.Client()
# bucket = storage_client.bucket("social-signals-datalake")

VENDOR = "finnhub"


def data_to_df(data):
    df = pd.DataFrame(data=data)
    df.index = pd.to_datetime(df.t, unit="s")
    return df


TIME_TEMPLATE = "%Y-%m-%d_%H%M%S"


def get_human_time() -> str:
    created_at = datetime.now(tz=pytz.UTC)
    return created_at.strftime(TIME_TEMPLATE)


def store_df_in_gs(symbol, df):
    day = datetime.now(tz=pytz.UTC).strftime("%Y-%m-%d")
    blob = bucket.blob(
        f"finnhub/common_stocks/ohcl_daily/{day}/{symbol}_{get_human_time()}"
    )
    blob.upload_from_string(df.to_csv())


async def get_ohcl_data_for(session, start, end, symbol: str, frequency: str = "D"):
    try:
        data = await get_ohcl_data_(session, start, end, frequency, symbol)
        if data is not None:
            return to_ohcl_table(data, symbol)
    except Exception as e:
        logger.exception(e)
        return


async def get_ohcl_data_(session, start: int, end: int, frequency, symbol):
    data = await get_stock_candle(
        session=session, symbol=symbol, resolution=frequency, from_=start, to=end
    )

    return None if data["s"] == "no_data" else data


async def get_ohcl_table_for(start: int, end: int, symbols: List[str], frequency: str):
    logger.info("Start fetching OHLC data")
    tables = []
    symbols_n = len(symbols)
    # Partition symbols into groups of 3 and then do concurrent call
    async with aiohttp.ClientSession() as session:
        for idx, symbol in progress_bar(enumerate(symbols), total=symbols_n):
            if idx % 100 == 0:
                logger.info(f"Remaining: {symbols_n - idx}")

            table = await get_ohcl_data_for(
                session, start, end, symbol, frequency=frequency
            )
            if isinstance(table, pa.Table):
                tables.append(table)
            else:
                logger.info(f"Skipping {symbol}")
        return pa.concat_tables(tables)


async def get_company_table_for(symbols: List[str]) -> pa.Table:
    logger.info("Start fetching company descriptions data")
    tables = []
    symbols_n = len(symbols)
    # Partition symbols into groups of 3 and then do concurrent call
    async with aiohttp.ClientSession() as session:
        for idx, symbol in progress_bar(enumerate(symbols), total=symbols_n):
            if idx % 100 == 0:
                logger.info(f"Remaining: {symbols_n - idx}")

            data = await get_company_profile(session, symbol)
            if data:
                table = to_company_description_table(data)
            else:
                logger.warn(f"Skipping {symbol}")
                continue
            if isinstance(table, pa.Table):
                tables.append(table)
            else:
                logger.info(f"Skipping {symbol}")
        return pa.concat_tables(tables)


def pull_ohcl_data(
    *,
    store,
    start: Timestamp,
    end: Timestamp,
    market: str,
    frequency: str,
    include_company_information: bool = True,
):
    company_table = None

    df_symbols, symbols = get_symbols_for(market)
    symbol_table = pa.Table.from_pandas(df_symbols, schema=STOCK_SYMBOL)

    start_timestamp = int(start.timestamp())
    end_timestamp = int(end.timestamp())

    if include_company_information:
        company_table = asyncio.run(get_company_table_for(symbols=symbols))

    table = asyncio.run(
        get_ohcl_table_for(start_timestamp, end_timestamp, symbols, frequency)
    )

    store.store(
        symbol_table=symbol_table,
        price_table=table,
        company_table=company_table,
        start=start,
        end=end,
        frequency=frequency,
        vendor=VENDOR,
    )
