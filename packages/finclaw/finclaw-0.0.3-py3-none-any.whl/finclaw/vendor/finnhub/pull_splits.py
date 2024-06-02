import asyncio
from typing import List

import aiohttp
import pandas as pd
import pyarrow as pa
from finclaw.utils.progress_bar import progress_bar

import finclaw.vendor.finnhub.finnhub_client as fc
from finclaw.vendor.finnhub import models


async def get_splits(
    symbols: List[str], start: pd.Timestamp, end: pd.Timestamp
) -> pa.Table:
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")

    result = []
    for symbol in progress_bar(symbols, desc="Pulling splits information:"):
        async with aiohttp.ClientSession() as session:
            split_records = await fc.get_stock_splits(
                session, symbol=symbol, from_=start, to=end
            )

            if table := models.to_split_data(split_records, symbol):
                result.append(table)

    return pa.concat_tables(result)


def pull_splits(*, store, symbols, start, end):
    splits_table = asyncio.run(get_splits(symbols, start, end))
    store.store_splits(split_table=splits_table, start=start, end=end, vendor="finnhub")
