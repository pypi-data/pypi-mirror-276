import asyncio
from typing import List

import aiohttp
import pandas as pd
import pyarrow as pa
from finclaw.utils.progress_bar import progress_bar

import finclaw.vendor.finnhub.finnhub_client as fc
from finclaw.vendor.finnhub import models


async def get_institutional_ownership_table(
    symbols: List[str], start: pd.Timestamp, end: pd.Timestamp
) -> pa.Table:
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")

    result = []
    for symbol in progress_bar(
        symbols, desc="Pulling institutional ownership information"
    ):
        async with aiohttp.ClientSession() as session:
            insider_transaction_records = await fc.get_institutional_ownership(
                session, symbol=symbol, from_=start, to=end
            )

            if table := models.to_institutional_ownership_table(
                insider_transaction_records
            ):
                result.append(table)

    return pa.concat_tables(result)


async def get_fund_ownership_table(symbols: List[str]) -> pa.Table:
    result = []
    for symbol in progress_bar(symbols, desc="Pulling fund ownership information"):
        async with aiohttp.ClientSession() as session:
            fund_ownership_record = await fc.get_fund_ownership(session, symbol=symbol)
            if table := models.to_fund_ownership_table(fund_ownership_record):
                result.append(table)

    return pa.concat_tables(result)


async def get_all_owners_table(symbols: List[str]) -> pa.Table:
    result = []
    for symbol in progress_bar(symbols, desc="Pull all owners data"):
        async with aiohttp.ClientSession() as session:
            all_owners_table = await fc.get_all_owners(session, symbol=symbol)
            if table := models.to_all_owners_table(all_owners_table):
                result.append(table)
    return pa.concat_tables(result)


def pull_ownership_data_for(*, store, symbols, start, end):
    institutional_ownership = asyncio.run(
        get_institutional_ownership_table(symbols, start, end)
    )
    fund_ownership = asyncio.run(get_fund_ownership_table(symbols))
    all_owners = asyncio.run(get_all_owners_table(symbols))

    store.store_ownership(
        institutional_ownership_table=institutional_ownership,
        fund_ownership_table=fund_ownership,
        all_owners_table=all_owners,
        start=start,
        end=end,
    )
