import asyncio

import aiohttp

from finclaw.config import logger
from finclaw.config import settings

API_BASE = "https://financialmodelingprep.com/api/v3/"


# 30 API/Seconds limit


async def _call_api(
    session, url: str, payload: str, querystring: dict, error_count=0
) -> dict:
    if settings.FMP_API_KEY == "":
        raise ValueError("You need to specify FMP_API_KEY")
    querystring["apikey"] = settings.FMP_API_KEY

    async with session.get(url, data=payload, params=querystring) as resp:
        if error_count >= 4:
            raise ValueError(f"Too many errors: {resp.status}")
        if resp.status != 200:
            logger.info("Rate limit reached going to sleep")
            await asyncio.sleep(60)
            return await _call_api(session, url, payload, querystring, error_count + 1)
        try:
            json_response = await resp.json()
        except aiohttp.ContentTypeError as e:
            logger.exception("Could not parse response")
        return json_response


async def get_symbols(session: aiohttp.ClientSession):
    querystring = {}
    return await _call_api(
        session,
        f"{API_BASE}stock/list",
        payload="",
        querystring={},
    )


async def get_stock_candle(
    session: aiohttp.ClientSession, symbol: str, resolution: str
):
    if resolution == "1":
        return await _call_api(
            session,
            f"{API_BASE}historical-chart/1min/{symbol}",
            payload="",
            querystring={},
        )
    else:
        raise NotImplementedError("Only 1 minute resolution is supported")


async def get_financials_for(
    session: aiohttp.ClientSession, symbol: str, statement: str, freq: str
):
    """
    https://site.financialmodelingprep.com/developer/docs#financial-statements
    """
    endpoint_map = {
        "bs": "balance-sheet-statement",
        "ic": "income-statement",
        "cf": "cash-flow-statement",
    }
    periods = ["annual", "quarter"]
    if statement not in endpoint_map:
        raise ValueError(f"statement:{statement} should be one of bs, ic, cf")
    if freq not in periods:
        raise ValueError(f"freq:{freq} should be one of {periods}")

    return await _call_api(
        session,
        f"{API_BASE}{endpoint_map[statement]}/{symbol}",
        payload="",
        querystring={"period": freq},
    )
