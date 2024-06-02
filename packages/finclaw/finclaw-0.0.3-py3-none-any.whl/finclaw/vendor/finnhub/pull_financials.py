import asyncio
from typing import List

import aiohttp
import pandas as pd
import pyarrow as pa
from pandas import Timestamp

from finclaw.config import settings, logger
from finclaw.data_store.store import PriceStore
from finclaw.vendor.finnhub.finnhub_client import get_financials_for
from finclaw.vendor.finnhub import models
from finclaw.vendor.finnhub.symbols import get_symbols_for
from finclaw.utils.progress_bar import progress_bar


async def get_financials(
    symbols: List[str], start: pd.Timestamp, end: pd.Timestamp, statement, freq
) -> pa.Table:
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    #  TODO:  This is going to be different for each symbol
    #  because the financials are different for each symbol
    result = []
    for symbol in progress_bar(symbols, desc="Pulling financials"):
        async with aiohttp.ClientSession() as session:
            financial_records = await get_financials_for(
                session, symbol=symbol, statement=statement, freq=freq
            )

            if statement == "bs":
                try:
                    if table := models.to_balance_sheet_financial_data(
                        financial_records
                    ):
                        result.append(table)
                except Exception as e:
                    logger.error(f"Error pulling balance sheet data for {symbol} {e}")
                    raise e
            elif statement == "ic":
                try:
                    if table := models.to_income_statement_financial_data(
                        financial_records
                    ):
                        result.append(table)
                except Exception as e:
                    logger.error(
                        f"Error pulling income statement data for {symbol} {e}"
                    )
                    raise e
            elif statement == "cf":
                try:
                    if table := models.to_cash_flow_financial_data(financial_records):
                        result.append(table)
                except Exception as e:
                    logger.error(f"Error pulling cash flow data for {symbol} {e}")
                    raise e
            else:
                raise ValueError(f"Unknown statement type {statement}")

    return pa.concat_tables(result)


def pull_financials(*, store, symbols, start: Timestamp, end: Timestamp):
    balance_sheet_table = asyncio.run(
        get_financials(symbols, start, end, "bs", "quarterly")
    )
    store.store_financials(
        statement="balance_sheet",
        financials_table=balance_sheet_table,
        start=start,
        end=end,
        vendor="finnhub",
    )

    income_statement_table = asyncio.run(
        get_financials(symbols, start, end, "ic", "quarterly")
    )
    store.store_financials(
        statement="income_statement",
        financials_table=income_statement_table,
        start=start,
        end=end,
        vendor="finnhub",
    )

    cashflow_statements = asyncio.run(
        get_financials(symbols, start, end, "cf", "quarterly")
    )
    store.store_financials(
        statement="cashflow_statement",
        financials_table=cashflow_statements,
        start=start,
        end=end,
        vendor="finnhub",
    )
