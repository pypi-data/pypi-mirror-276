import asyncio
from typing import List

import aiohttp
import pandas as pd
import pyarrow as pa
from pandas import Timestamp
from finclaw.utils.progress_bar import progress_bar

from finclaw.config import logger
from finclaw.vendor.finnhub import models
from finclaw.vendor.finnhub.finnhub_client import get_dividend


async def get_dividends(
    symbols: List[str], start: pd.Timestamp, end: pd.Timestamp
) -> pa.Table:
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")

    result = []
    for symbol in progress_bar(symbols, desc="Pulling dividend information"):
        try:
            async with aiohttp.ClientSession() as session:
                symbol_dividend_records = await get_dividend(
                    session, symbol=symbol, from_=start, to=end
                )
                if table := models.to_dividend_table(symbol_dividend_records):
                    result.append(table)
        except Exception as e:
            logger.info(f"Error pulling dividend data for {symbol} {e}")

    return pa.concat_tables(result)


def pull_dividend_data(*, store, symbols, start: Timestamp, end: Timestamp):
    dividend_table = asyncio.run(get_dividends(symbols, start, end))
    store.store_dividends(
        dividend_table=dividend_table, start=start, end=end, vendor="finnhub"
    )
