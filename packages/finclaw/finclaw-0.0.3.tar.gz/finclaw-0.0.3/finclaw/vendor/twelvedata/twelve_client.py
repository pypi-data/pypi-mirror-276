import asyncio
import re
from typing import Optional, List

import aiohttp

from finclaw.config import logger
from finclaw.config import settings
from finclaw.vendor.exceptions import NotSuccessfull

API_BASE = "https://api.twelvedata.com/"


# 30 API/Seconds limit


async def _call_api(
    session, url: str, payload: str, querystring: dict, error_count=0
) -> Optional[dict]:
    if settings.FMP_API_KEY == "":
        raise ValueError("You need to specify TWELVEDATA_API_KEY")
    querystring["apikey"] = settings.TWELVEDATA_API_KEY
    logger.debug(f"Calling {url} with {querystring}")
    del querystring["mic_code"]
    async with session.get(url, data=payload, params=querystring) as resp:
        logger.debug(f"Calling {url} with {querystring}")
        try:
            json_response = await resp.json()
            logger.debug(f"Response: {json_response}")
            if return_code := json_response.get("code", None):
                if return_code == 429:
                    if error_count > 5:
                        raise NotSuccessfull("Too many errors")
                    logger.warning("Rate limit reached going to sleep")
                    await asyncio.sleep(60)
                    return await _call_api(
                        session, url, payload, querystring, error_count=error_count + 1
                    )
                elif return_code == 404:
                    logger.warning(f"Not found:{json_response}")
                    return None
                else:
                    raise NotSuccessfull(f"Error code: {return_code}")

        except aiohttp.ContentTypeError as e:
            logger.exception("Could not parse response")
        return json_response


async def get_symbols(session: aiohttp.ClientSession):
    querystring = {}
    return await _call_api(
        session,
        f"{API_BASE}stocks",
        payload="",
        querystring={},
    )


async def get_stock_candle(
    session: aiohttp.ClientSession, *, symbol: str, resolution: str, mic_code: str
):
    """
    5min, 15min, 30min, 45min, 1h, 2h, 4h, 1day, 1week, 1month
    Parameters
    ----------
    session
    symbol
    resolution
    mic_code

    Returns
    -------

    """
    if resolution == "1":
        return await _call_api(
            session,
            f"{API_BASE}time_series",
            payload="",
            querystring={
                "interval": "1min",
                "symbol": symbol,
                "mic_code": mic_code,
            },
        )
    elif resolution == "D":
        return await _call_api(
            session,
            f"{API_BASE}time_series",
            payload="",
            querystring={
                "interval": "1day",
                "symbol": symbol,
                "mic_code": mic_code,
            },
        )
    else:
        raise NotImplementedError("Only 1 minute resolution is supported")
