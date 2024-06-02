import asyncio
import re
from typing import Optional, List

import aiohttp

from finclaw.config import logger
from finclaw.config import settings
from finclaw.vendor.exceptions import NotSuccessfull

API_BASE = "https://finnhub.io/api/v1/"


# 30 API/Seconds limit

async def _call_api(session, url: str, payload: str, querystring: dict, error_count=0) -> dict:
    if settings.FINNHUB_API == "":
        raise ValueError("You need to specify FINNHUB_API")
    querystring["token"] = settings.FINNHUB_API
    async with session.get(url, data=payload, params=querystring) as resp:
        try:
            json_response = await resp.json()
        except aiohttp.ContentTypeError as e:
            logger.exception("Could not parse response")
            text = await resp.text()
            if "Too Many Requests" in text:
                logger.info("Rate limit reached going to sleep")
                await asyncio.sleep(60)
                return await _call_api(session, url, payload, querystring)
            else:
                logger.info(text)
                logger.info(resp.status)
                logger.info(resp.headers)
                if error_count >= 4:
                    raise e

                await asyncio.sleep(30)
                return await _call_api(session, url, payload, querystring, error_count + 1)

        rate_limit = resp.headers.get("X-Ratelimit-Remaining")

        if resp.status != 200:
            logger.info(await resp.json())
            logger.info(resp.status)
            logger.info(resp.headers)
            raise NotSuccessfull()

        if rate_limit is None:
            logger.exception("Rate limit is None something is wrong")
            logger.info(resp.headers)
            logger.info(resp.json())
            logger.info(resp.status)

        if int(rate_limit) <= 4:
            logger.info("Rate limit reached going to sleep")
            await asyncio.sleep(60)
            return await _call_api(session, url, payload, querystring)
        return json_response


async def get_symbols(session: aiohttp.ClientSession, exchange: str, mic: Optional[str] = None):
    querystring = {}
    if mic is not None:
        querystring["mic"] = mic
    querystring["exchange"] = exchange
    json_response = await _call_api(session, f"{API_BASE}stock/symbol", payload="", querystring=querystring)

    return json_response


async def get_stock_candle(session: aiohttp.ClientSession, symbol: str, resolution: str, from_: int, to: int):
    assert from_ < to
    querystring = {"symbol": symbol, "resolution": resolution, "from": str(from_), "to": str(to)}

    json_response = await _call_api(session, f"{API_BASE}stock/candle", payload="", querystring=querystring)

    return json_response


async def get_company_profile(session: aiohttp.ClientSession, symbol: str):
    """
    Implementation over https://finnhub.io/docs/api/company-profile2
    :param session:
    :param symbol:
    :return:
    """
    querystring = {"symbol": symbol}
    json_response = await _call_api(session, f"{API_BASE}stock/profile", payload="", querystring=querystring)

    return json_response


async def get_dividend(session: aiohttp.ClientSession, *, symbol: str, from_: str, to: str) -> List[dict]:
    """
    Implementation over https://finnhub.io/docs/api/stock-dividends
    Args:
        session ClientSession:
        symbol str: Stock symbol
        from_:
        to:

    Returns:
        [
          {
            "symbol": "AAPL",
            "date": "2019-05-10", # ex-dividend date
            "amount": 0.77,
            "adjustedAmount": 0.77,
            "payDate": "2019-05-16",
            "recordDate": "2019-05-13",
            "declarationDate": "2019-05-01",
            "currency": "USD"
          },
          ...
        ]
    Notes:
        ## Ex-dividend date
            The ex-dividend date for stocks is usually set one business day before the record date.
            If you purchase a stock on its ex-dividend date or after, you will not receive the next dividend payment.
            Instead, the seller gets the dividend. If you purchase before the ex-dividend date, you get the dividend.

        ## Record date
            The date of record is the date in which the company identifies all of its current stockholders,
            and therefore everyone who is eligible to receive the dividend.
            If you're not on the list, you don't get the dividend.
    """
    if not is_valid_format(from_) and is_valid_format(to):
        raise ValueError(f"from_:{from_} and to:{to} should be in YYYY-MM-DD format")

    querystring = {"symbol": symbol, "from": from_, "to": to}
    return await _call_api(
        session,
        f"{API_BASE}stock/dividend",
        payload="",
        querystring=querystring,
    )


def is_valid_format(from_) -> bool:
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    match = re.match(pattern, from_)
    return match is not None


async def get_insider_transactions(session: aiohttp.ClientSession, symbol: str):
    """

    Args:
        session:
        symbol:

    Returns:
        [
            {
              "name": "Kirkhorn Zachary",
              "share": 57234,
              "change": -1250,
              "filingDate": "2021-03-19",
              "transactionDate": "2021-03-17",
              "transactionCode": "S",
              "transactionPrice": 655.81
            },
            ...
        ]
    """
    return await _call_api(session, f"{API_BASE}stock/insider-transactions", payload="", querystring={"symbol": symbol})


async def get_institutional_ownership(session: aiohttp.ClientSession, symbol: str, from_: str, to: str):
    """

    Args:
        session:
        symbol:
        from_:
        to:

    Returns:
        [
    """
    if not is_valid_format(from_) and is_valid_format(to):
        raise ValueError(f"from_:{from_} and to:{to} should be in YYYY-MM-DD format")

    return await _call_api(session, f"{API_BASE}institutional/ownership", payload="",
                           querystring={"symbol": symbol, "from": from_, "to": to})


async def get_fund_ownership(session: aiohttp.ClientSession, symbol: str):
    """

    Args:
        session:
        symbol:

    Returns:
    {
      "ownership": [
        {
          "name": "AGTHX | American Funds Growth Fund of America",
          "share": 5145353,
          "change": 57427,
          "filingDate": "2020-03-31",
          "portfolioPercent": 1.88
        },
        {
          "name": "Vanguard Total Stock Market Index Fund",
          "share": 4227464,
          "change": 73406,
          "filingDate": "2020-03-31",
          "portfolioPercent": 0.45
        },
        {
          "name": "ANWPX | American Funds New Perspective",
          "share": 3377612,
          "change": 0,
          "filingDate": "2020-03-31",
          "portfolioPercent": 2.64
        }
      ],
      "symbol": "TSLA"
    }
    """
    return await _call_api(session, f"{API_BASE}stock/fund-ownership", payload="", querystring={"symbol": symbol})


async def get_all_owners(session: aiohttp.ClientSession, symbol: str):
    """

    Args:
        session:
        symbol:

    Returns:
    {
      "ownership": [
        {
          "name": "AGTHX | American Funds Growth Fund of America",
          "share": 5145353,
          "change": 57427,
          "filingDate": "2020-03-31",
          "portfolioPercent": 1.88
        },
        {
          "name": "Vanguard Total Stock Market Index Fund",
          "share": 4227464,
          "change": 73406,
          "filingDate": "2020-03-31",
          "portfolioPercent": 0.45
        },
        {
          "name": "ANWPX | American Funds New Perspective",
          "share": 3377612,
          "change": 0,
          "filingDate": "2020-03-31",
          "portfolioPercent": 2.64
        }
      ],
      "symbol": "TSLA"
    }
    """
    return await _call_api(session, f"{API_BASE}stock/ownership", payload="", querystring={"symbol": symbol})


async def get_financials_for(session: aiohttp.ClientSession, symbol: str, statement: str, freq: str):
    """

    Args:
        session:
        symbol:
        statement:
        freq:

    Returns:

    """
    if statement not in ["bs", "ic", "cf"]:
        raise ValueError(f"statement:{statement} should be one of bs, ic, cf")

    if freq not in ["annual", "quarterly", "ttm", "ytd"]:
        raise ValueError(f"freq:{freq} should be one of annual, quarterly")

    return await _call_api(session,
                           f"{API_BASE}stock/financials",
                           payload="",
                           querystring={"symbol": symbol, "statement": statement, "freq": freq})


async def get_stock_splits(session: aiohttp.ClientSession, symbol: str, from_: str, to: str):
    """

    Args:
        session:
        symbol:
        from_:
        to:

    Returns:
        [
          {
            "date": "2014-06-09",
            "fromFactor": 1,
            "toFactor": 7,
          },
          ...
        ]
    """
    if not is_valid_format(from_) and is_valid_format(to):
        raise ValueError(f"from_:{from_} and to:{to} should be in YYYY-MM-DD format")

    return await _call_api(session, f"{API_BASE}stock/split", payload="",
                           querystring={"symbol": symbol, "from": from_, "to": to})
