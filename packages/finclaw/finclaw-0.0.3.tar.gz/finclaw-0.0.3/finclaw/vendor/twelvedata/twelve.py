import asyncio
from typing import List, Optional

import aiohttp
import pandas as pd
import pyarrow as pa
import pytz
from pandas import Timestamp

from finclaw.config import logger
from finclaw.data_store.schema import OHCL, STOCK_SYMBOL
from finclaw.data_store.store import PriceStore
from finclaw.data_store.storeV2 import PriceStoreV2
from finclaw.utils.progress_bar import progress_bar
from finclaw.vendor.twelvedata import twelve_client as twclient

VENDOR = "twelvedata"


async def get_symbols(session: aiohttp.ClientSession, market: str) -> pd.DataFrame:
    symbols = await twclient.get_symbols(session=session)
    data = filter(lambda x: x["mic_code"] == market, symbols["data"])
    df = pd.DataFrame(data=data)
    df = df.rename(
        columns={
            "symbol": "ticker",
            "name": "description",
            "currency": "currency_name",
            "mic_code": "mic",
        }
    )
    df["figi"] = None
    return df[STOCK_SYMBOL.names]


async def get_ohcl_for_symbol(
    session: aiohttp.ClientSession, *, symbol: str, resolution: str, mic_code: str
) -> Optional[pd.DataFrame]:
    ohcl_json = await twclient.get_stock_candle(
        session=session, symbol=symbol, resolution=resolution, mic_code=mic_code
    )
    if not ohcl_json:
        return None
    df = pd.DataFrame(data=ohcl_json["values"])
    df["timestamp"] = pd.to_datetime(df["datetime"]).dt.tz_localize("America/New_york")
    df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")
    df["symbol"] = symbol

    df[["open", "high", "close", "low"]] = df[["open", "high", "close", "low"]].astype(
        float
    )
    df["volume"] = df["volume"].astype(int)

    return df[OHCL.names]


async def get_ohcl_data(
    session: aiohttp.ClientSession,
    *,
    start: Timestamp,
    end: Timestamp,
    symbols: List[str],
    frequency: str,
    mic_code: str,
) -> pd.DataFrame:
    if start > end:
        raise ValueError("Start date cannot be greater than end date")
    if start.tz != pytz.UTC or end.tz != pytz.UTC:
        raise ValueError("Start and end dates must be UTC")

    dfs = []
    for symbol in progress_bar(symbols):
        symbol_df = await get_ohcl_for_symbol(
            session=session, symbol=symbol, resolution=frequency, mic_code=mic_code
        )
        if symbol_df is not None:
            dfs.append(symbol_df)

    result_df = pd.concat(dfs)
    return result_df[(result_df.timestamp >= start) & (result_df.timestamp <= end)]


async def get_symbol_table(market_id_code: str) -> pa.Table:
    async with aiohttp.ClientSession() as session:
        symbol_df = await get_symbols(session=session, market=market_id_code)
        return pa.Table.from_pandas(symbol_df, schema=STOCK_SYMBOL)


async def get_ohcl_table_for(
    start: Timestamp,
    end: Timestamp,
    symbols: List[str],
    frequency: str,
    market_id_code: str,
) -> pa.Table:
    async with aiohttp.ClientSession() as session:
        ohcl_df = await get_ohcl_data(
            session=session,
            start=start,
            end=end,
            symbols=symbols,
            frequency=frequency,
            mic_code=market_id_code,
        )
        return pa.Table.from_pandas(ohcl_df, schema=OHCL)


def pull_symbols(
    *, store: PriceStoreV2, market_id_code: str, start: pd.Timestamp, end: pd.Timestamp
):
    symbol_table = asyncio.run(get_symbol_table(market_id_code=market_id_code))
    store.store_symbols(symbol_table=symbol_table, start=start, end=end)


def pull_ohcl_data(
    *,
    store: PriceStoreV2,
    symbols: List[str],
    start: Timestamp,
    end: Timestamp,
    frequency: str,
    market_id_code: str,
):
    table = asyncio.run(
        get_ohcl_table_for(
            start, end, symbols, frequency, market_id_code=market_id_code
        )
    )
    store.store_prices(price_table=table, start=start, end=end, frequency=frequency)
