import asyncio

import click
import pandas as pd
from pandas import Timestamp

from finclaw.config import settings, logger
from finclaw.data_store.storage_clients import S3StoreClient
from finclaw.data_store.storage_clients.LocalStoreClient import LocalStoreClient
from finclaw.data_store.store import PriceStore
from finclaw.data_store.storeV2 import PriceStoreV2
from finclaw.utils.cli_utils import Date
from finclaw.vendor import twelvedata as twelve
from finclaw.vendor.finnhub.pull_dividends import pull_dividend_data
from finclaw.vendor.finnhub.pull_financials import pull_financials
from finclaw.vendor.finnhub.pull_insider_information import pull_insider_information
from finclaw.vendor.finnhub.pull_ohcl import pull_ohcl_data
from finclaw.vendor.finnhub.pull_ownership import pull_ownership_data_for
from finclaw.vendor.finnhub.pull_splits import pull_splits
from finclaw.vendor.finnhub.symbols import get_symbols_for
from finclaw.vendor.fmp import fmp
from typing import Optional, List


@click.group
def main():
    pass


def fmp_vendor(
    *,
    store,
    frequency,
    include_information,
    market,
    start: pd.Timestamp,
    end: pd.Timestamp,
    symbol: Optional[List[str]] = None,
):
    include_information = include_information.split(",")
    if not symbol:
        symbols: List[str] = (
            asyncio.run(fmp.get_symbol_table(market=market)).to_pandas().ticker.values
        )
    else:
        symbols: List[str] = symbol

    if "p" in include_information:
        fmp.pull_symbols(store=store, market=market, start=start, end=end)
        fmp.pull_ohcl_data(
            store=store, symbols=symbols, start=start, end=end, frequency=frequency
        )

    financial_statements = {"bs", "ic", "cf"} & set(include_information)
    if financial_statements:
        fmp.pull_financials(
            store=store,
            symbols=symbols,
            start=start,
            end=end,
            statements=financial_statements,
        )


def twelve_data_vendor(
    *,
    store,
    frequency: str,
    include_information: str,
    market_id_code: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
    symbols,
):
    if "p" in include_information:
        if not symbols:
            symbols = (
                asyncio.run(twelve.get_symbol_table(market_id_code=market_id_code))
                .to_pandas()
                .ticker.values
            )
            twelve.pull_symbols(
                store=store, market_id_code=market_id_code, start=start, end=end
            )
        else:
            symbols = symbols

        twelve.pull_ohcl_data(
            store=store,
            symbols=symbols,
            start=start,
            end=end,
            frequency=frequency,
            market_id_code=market_id_code,
        )
    else:
        raise NotImplementedError()


@main.command()
@click.option(
    "-s",
    "--start",
    type=Date(tz="utc", as_timestamp=False),
    help="The start date from which to pull data.",
    required=True,
)
@click.option(
    "-e",
    "--end",
    type=Date(tz="utc", as_timestamp=False),
    help="The end date from which to pull data.",
    required=True,
)
@click.option(
    "-f",
    "--frequency",
    type=click.Choice(["1", "5", "15", "30", "60", "D", "W", "M"]),
    help="What's the frequency the data should be.",
    required=True,
)
@click.option(
    "-m",
    "--market",
    type=click.Choice(["US", "TO"]),
    help="What's the market to use?",
    required=False,
)
@click.option(
    "-mic", "--market-id-code", help="Market identification code", required=False
)
@click.option(
    "-ic", "--include-information", help="Information to include", required=True
)
@click.option(
    "-v",
    "--vendor",
    type=click.Choice(["finnhub", "fmp", "twelvedata"]),
    help="Vendor to use",
    required=True,
)
@click.option("-s", "--symbol", help="Vendor to use", multiple=True, required=False)
@click.option(
    "-storage",
    "--storage-type",
    type=click.Choice(["s3", "local", "gs"]),
    help="Storage backend to use",
    required=False,
)
@click.option("-r", "--region", help="AWS region to use", required=False)
@click.option("-b", "--bucket-name", help="Bucket name", required=False)
def grab(
    start: Timestamp,
    end: Timestamp,
    frequency: str,
    market: str,
    include_information: str,
    vendor: str,
    market_id_code: str,
    symbol: Optional[List[str]],
    storage_type: Optional[str],
    region: Optional[str],
    bucket_name: Optional[str],
) -> None:
    """
    Grabs data from a vendor and storage_clients it on local
    :param start: Normalized (floor down) so 2012-01-01T12:15:16 -> 2012-01-01T00:00:00
    :param end: Same as start

    Args:
        include_company_information:
        market: Market to pull data from: US, TO ...
        frequency: Granularity of the data: 1, 5, 15, 30, 60, D, W, M
    """
    if storage_type.lower() == "s3":
        if bucket_name is None and region is None:
            raise ValueError(
                "When using s3 as storage backend you must specify bucket name and region"
            )
        storage_client = S3StoreClient(bucket_name=bucket_name, region=region)
        store = PriceStoreV2(settings.TRADE_ENGINE_DATA, storage_client, vendor=vendor)
    else:
        storage_client = LocalStoreClient()
        store = PriceStoreV2(settings.TRADE_ENGINE_DATA, storage_client, vendor=vendor)
    logger.info(f"Storage path: {settings.TRADE_ENGINE_DATA}")

    if vendor == "finnhub":
        finnhub_vendor(store, end, frequency, include_information, market, start)
    elif vendor == "fmp":
        fmp_vendor(
            store=store,
            frequency=frequency,
            include_information=include_information,
            market=market,
            start=start,
            end=end,
            symbol=symbol,
        )
    elif vendor == "twelvedata":
        twelve_data_vendor(
            store=store,
            frequency=frequency,
            include_information=include_information,
            market_id_code=market_id_code,
            start=start,
            end=end,
            symbols=symbol,
        )


def finnhub_vendor(store, end, frequency, include_information, market, start):
    _, symbols = get_symbols_for(market)
    if "o" in include_information:
        pull_ownership_data_for(store=store, symbols=symbols, start=start, end=end)
    if "i" in include_information:
        pull_insider_information(store=store, symbols=symbols, start=start, end=end)
    if "f" in include_information:
        pull_financials(store=store, symbols=symbols, start=start, end=end)
    if "d" in include_information:
        pull_dividend_data(store=store, symbols=symbols, start=start, end=end)
    if "s" in include_information:
        pull_splits(store=store, symbols=symbols, start=start, end=end)
    if "p" in include_information:
        include_company_information = "c" in include_information
        pull_ohcl_data(
            store=store,
            start=start,
            end=end,
            frequency=frequency,
            market=market,
            include_company_information=include_company_information,
        )


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://wfw.jetbrains.com/hetp/pycharm/
