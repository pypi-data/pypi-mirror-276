import asyncio
from typing import List

import aiohttp
import pandas as pd

from finclaw.vendor.finnhub.finnhub_client import get_symbols


async def get_symbols_to_pull(market: str) -> pd.DataFrame:
    async with aiohttp.ClientSession() as session:
        symbols = await get_symbols(session, exchange=market)
        return pd.DataFrame(symbols)


def get_symbols_for(market) -> (pd.DataFrame, List[str]):
    df_symbols = asyncio.run(get_symbols_to_pull(market))
    df_symbols = df_symbols[["currency", "description", "mic", "symbol", "figi", "type"]]
    df_symbols = df_symbols.rename(columns={"symbol": "ticker", "currency": "currency_name"})
    # ETP Exchange Traded Product
    df_stocks_to_pull = df_symbols[df_symbols.type.isin(["Common Stock", "ETP", "REIT"])]
    symbols = df_stocks_to_pull.ticker.values
    return df_symbols, symbols
