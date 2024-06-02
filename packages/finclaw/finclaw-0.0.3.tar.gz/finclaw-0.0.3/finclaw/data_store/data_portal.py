import os
from collections import namedtuple
from datetime import timedelta
from typing import List, Optional, Union, Dict

import pandas as pd
import pyarrow as pa

from finclaw.data_store.storeV2 import PriceStoreV2
from finclaw.utils.progress_bar import progress_bar

from finclaw.config import settings
from finclaw.data_store.store import PriceStore
from finclaw.data_store.validators import validate_vendor

DataChunk = namedtuple("DataChunk", ["current_date", "price_ohcl_daily"])


class Snapshot:
    def __init__(self, df: pd.DataFrame):
        self.data = df

    def history(self, days: int):
        """
        Get dataframe for the last n days
        :param days:
        :return:
        """
        return self.data[
            (self.data.index.max() - pd.Timedelta(days=days)) <= self.data.index
        ]


class DataPortal:
    """
    This is used by the simulation runner to answer questions about the data,
    like getting the prices of assets on a given day or to service history
    calls.
    """

    def __init__(
        self, price_store: PriceStore, start: pd.Timestamp, end: pd.Timestamp, step
    ):
        self.price_data: Optional[pd.DataFrame] = None
        self._price_store = price_store
        self.current_date: pd.Timestamp = start
        self.start = start
        self.end = end
        self.step = step

    def load_price_data(
        self, *, start: pd.Timestamp, end: pd.Timestamp, frequency: str, vendor: str
    ) -> pa.Table:
        return self._price_store.load_prices(start=start, end=end, frequency=frequency)

    def init(self):
        price = self.load_price_data(
            start=self.start, end=self.end, frequency="D", vendor="finnhub"
        )
        df = price.to_pandas()
        df.index = df.timestamp
        self.price_data = df

    def get_simulation_data_frames(self):
        end = self.end
        while self.current_date < end:
            yield self.get_snapshot(current_date=self.current_date)
            self.current_date = self.current_date + timedelta(days=self.step)

    def get_snapshot(self, *, current_date: pd.Timestamp):
        if self.price_data is None:
            raise ValueError("You need to call initialize")

        # Note, we want a copy
        price_df = self.price_data[self.price_data.index <= current_date]

        return DataChunk(
            current_date=self.current_date, price_ohcl_daily=Snapshot(price_df)
        )


def list_stores(
    path=settings.TRADE_ENGINE_DATA, is_dict=False
) -> Union[List[PriceStore], Dict[str, PriceStore]]:
    if not is_dict:
        return [PriceStore(path + "/" + ps_path) for ps_path in os.listdir(path)]
    result = {}
    for ps_path in os.listdir(path):
        ps = PriceStore(path + "/" + ps_path)
        result[f"{repr(ps)}"] = ps
    return result


def list_stores_s3(
    storage_client, path=settings.TRADE_ENGINE_DATA, is_dict=False
) -> Union[List[PriceStoreV2], Dict[str, PriceStoreV2]]:
    if not is_dict:
        return [
            PriceStoreV2(path + "/" + ps_path, storage_client)
            for ps_path in storage_client.listdir(path)
        ]
    result = {}
    for ps_path in storage_client.listdir(path):
        ps = PriceStoreV2(path + "/" + ps_path, storage_client)
        result[f"{repr(ps)}"] = ps
    return result


def get_ohclv(
    store: Union[PriceStore, List[PriceStore]], *, frequency: str, vendor: str
) -> pa.Table:
    """
    Args:
        vendor:
        store:
        frequency:
    """
    validate_vendor(vendor)

    if isinstance(store, PriceStore):
        price = store.load_prices(frequency=frequency)

    elif isinstance(store, list):
        price = pa.concat_tables(
            [
                get_ohclv(
                    s,
                    frequency=frequency,
                    vendor=vendor,
                )
                for s in progress_bar(store)
            ]
        )
    else:
        raise ValueError("store needs to be a PriceStore or a List[PriceStore]")

    return price


def get_financials(
    store: Union[PriceStore, List[PriceStore]], *, vendor: str, statement_type: str
) -> pa.Table:
    validate_vendor(vendor)
    if isinstance(store, PriceStore):
        financials = store.load_financials(vendor=vendor, statement_type=statement_type)
    elif isinstance(store, list):
        financials = pa.concat_tables(
            [
                get_financials(
                    s,
                    vendor=vendor,
                    statement_type=statement_type,
                )
                for s in progress_bar(store)
            ]
        )
    else:
        raise ValueError("store needs to be a PriceStore or a List[PriceStore]")
    return financials


def get_insiders(store: Union[PriceStore, List[PriceStore]], *, vendor) -> pa.Table:
    validate_vendor(vendor)
    if isinstance(store, PriceStore):
        insiders = store.load_insiders(vendor=vendor)
    elif isinstance(store, list):
        insiders = pa.concat_tables(
            [get_insiders(s, vendor=vendor) for s in progress_bar(store)]
        )
    else:
        raise ValueError("store needs to be a PriceStore or a List[PriceStore]")
    return insiders
