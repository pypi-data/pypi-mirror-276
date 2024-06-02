import asyncio
from typing import List

import aiohttp
import pyarrow as pa
from finclaw.utils.progress_bar import progress_bar

from finclaw.vendor.finnhub import models
from finclaw.vendor.finnhub.finnhub_client import get_insider_transactions


async def get_insider_information_table(symbols: List[str]) -> pa.Table:
    result = []
    for symbol in progress_bar(symbols, desc="Pulling insider information"):
        async with aiohttp.ClientSession() as session:
            insider_transaction_records = await get_insider_transactions(
                session, symbol=symbol
            )
            data_to_process = insider_transaction_records["data"]
            if table := models.to_insider_table(data_to_process):
                result.append(table)

    return pa.concat_tables(result)


def pull_insider_information(*, store, symbols, start, end):
    insider_information = asyncio.run(get_insider_information_table(symbols))

    store.store_insider_information(
        insider_table=insider_information, start=start, end=end, vendor="finnhub"
    )
