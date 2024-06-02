import os
from typing import List, Optional

import pandas as pd
import pyarrow as pa
from pyarrow import parquet as pq
from pathlib import Path
from google.cloud import storage
import boto3
import os
from pyarrow import fs
from finclaw.data_store.schema import OHCL

"""
These are the storage_clients that are responsible for storing normalized data
"""


class VendorStore:
    def __init__(self, vendor_path):
        self._vendor_path = vendor_path
        self._company_description = "company_descriptions"

    def list_company_descriptions(self) -> List[str]:
        return list(os.listdir(self._vendor_path / self._company_description))

    def get_company_description_table(self) -> pd.DataFrame:
        for f in self.list_company_descriptions():
            return pq.read_table(
                self._vendor_path / self._company_description / f
            ).to_pandas()

    def list_available_resources(self):
        return list(os.listdir(self._vendor_path))

    def get_symbol_table(self):
        pass


class PriceStore:
    def __init__(self, path_to_price_store: str):
        self._price_path: Path = Path(path_to_price_store)

    def list_datasets(self):
        return os.listdir(self._price_path)

    # Loading logic
    def load_prices(
        self,
        *,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
        frequency: str,
    ) -> pa.Table:
        # sourcery skip: inline-immediately-returned-variable
        """
            Load prices from storage from start and end if exist
        :return:
        """
        if start is not None and end is not None:
            assert start < end
        self.path_exists()

        # Note: we can update this later to add filtering
        price_store = self.get_ohclv_price_store_path(frequency=frequency)

        if start and end:
            price_dataset_name = PriceStore.get_dataset_name(start=start, end=end)
            return self.load_table(price_dataset_name, price_store, schema=OHCL)
        else:
            tables = []
            for table_name in os.listdir(price_store):
                table_for_one_freq = self.load_table(
                    table_name, price_store, schema=OHCL
                )
                tables.append(table_for_one_freq)
            return pa.concat_tables(tables)

    def load_table(self, price_dataset, price_store, *, schema: pa.Schema) -> pa.Table:
        price_path = price_store / price_dataset
        if not price_path.exists():
            raise ValueError(f"{price_path} does not exist")
        dataset = pq.ParquetDataset(price_path, use_legacy_dataset=False, schema=schema)
        table: pa.Table = dataset.read()
        return table

    def load_symbols(
        self, *, start: pd.Timestamp, end: pd.Timestamp, vendor: str
    ) -> pa.Table:
        assert start < end
        self.path_exists()

        # Note: we can update this later to add filtering
        symbol_store_path = self.get_symbol_store_path(vendor=vendor)
        symbol_dataset = PriceStore.get_dataset_name(start=start, end=end)

        symbol_path = symbol_store_path / symbol_dataset

        if not symbol_path.exists():
            raise ValueError(f"{symbol_path} does not exist")

        dataset = pq.ParquetDataset(symbol_path, use_legacy_dataset=False)
        return dataset.read()

    def load_financials(self, statement_type: str):
        self.path_exists()

        financial_store_path = self.get_financial_statement_store_path(
            statement_type=statement_type
        )
        dataset = pq.ParquetDataset(financial_store_path, use_legacy_dataset=False)
        return dataset.read()

    def load_insiders(self, vendor):
        self.path_exists()

        insider_store_path = self.get_insider_store_path(vendor=vendor)
        dataset = pq.ParquetDataset(insider_store_path, use_legacy_dataset=False)
        return dataset.read()

    def path_exists(self):
        if not self._price_path.exists():
            raise ValueError(f"{self._price_path} does not exist")

    ## Store logic
    def store(
        self,
        *,
        symbol_table: pa.Table,
        price_table: pa.Table,
        start: pd.Timestamp,
        end: pd.Timestamp,
        frequency: str,
        vendor: str,
        company_table: Optional[pa.Table] = None,
    ):
        # Need to store symbols into a table as well
        self.store_prices(
            end=end,
            frequency=frequency,
            price_table=price_table,
            start=start,
            vendor=vendor,
        )
        self.store_symbols(
            symbol_table=symbol_table, start=start, end=end, vendor=vendor
        )
        if company_table:
            self.store_company_descriptions(
                company_table=company_table, start=start, end=end, vendor=vendor
            )

    def store_prices(self, *, end, frequency, price_table, start, vendor):
        price_store_ds = self.get_ohclv_price_store_path(frequency)
        self._save_table(price_store_ds, price_table, start, end)

    def store_symbols(
        self, *, symbol_table, start: pd.Timestamp, end: pd.Timestamp, vendor
    ):
        processing_date = pd.Timestamp.utcnow()
        n_rows = symbol_table.shape[0]
        symbol_table.add_column(
            0, "meta_storage_date", [[processing_date for i in range(n_rows)]]
        )

        symbol_store_ds = self.get_symbol_store_path(vendor=vendor)
        self._save_table(symbol_store_ds, symbol_table, start, end)

    def store_company_descriptions(self, *, company_table, start, end, vendor: str):
        company_descriptions = self.get_company_descriptions(vendor=vendor)
        self._save_table(company_descriptions, company_table, start, end)

    def store_ownership(
        self,
        *,
        institutional_ownership_table: pa.Table,
        fund_ownership_table: pa.Table,
        all_owners_table: pa.Table,
        start,
        end,
        vendor: str,
    ):
        fund_ownership_path = self.get_ownership_store_path("fund", vendor)
        self._save_table(fund_ownership_path, fund_ownership_table, start, end)

        institutional_ownership_path = self.get_ownership_store_path(
            "institutional", vendor
        )
        self._save_table(
            institutional_ownership_path, institutional_ownership_table, start, end
        )

        all_owners_path = self.get_ownership_store_path("all_owners", vendor)
        self._save_table(all_owners_path, all_owners_table, start, end)

    def store_insider_information(self, *, insider_table, start, end, vendor):
        insider_store_path = self.get_insider_store_path(vendor)
        self._save_table(insider_store_path, insider_table, start, end)

    def store_dividends(self, *, dividend_table, start, end, vendor):
        dividend_store_path = self.get_dividend_store_path(vendor)
        self._save_table(dividend_store_path, dividend_table, start, end)

    def store_financials(self, statement, financials_table, start, end, vendor):
        statement_store_path = self.get_financial_statement_store_path(
            vendor, statement
        )
        self._save_table(statement_store_path, financials_table, start, end)

    def store_splits(self, split_table, start, end, vendor):
        split_store_path = self.get_split_store_path(vendor)
        self._save_table(split_store_path, split_table, start, end)

    def get_symbol_store_path(self, *, vendor: str):
        return self._price_path / vendor / "symbols"

    def get_company_descriptions(self, *, vendor: str):
        return self._price_path / vendor / "company_descriptions"

    def get_ohclv_price_store_path(self, frequency):
        return self._price_path / "ohclv" / f"frequency_{frequency}"

    def get_ownership_store_path(self, ownership_type, vendor):
        return self._price_path / vendor / "ownership" / ownership_type

    def get_insider_store_path(self, vendor):
        return self._price_path / vendor / "insider"

    def get_dividend_store_path(self, vendor):
        return self._price_path / vendor / "dividends"

    def get_financial_statement_store_path(self, statement_type):
        return self._price_path / statement_type

    def get_split_store_path(self, vendor):
        return self._price_path / vendor / "splits"

    @staticmethod
    def _save_table(path_to_ds: Path, table, start: pd.Timestamp, end: pd.Timestamp):
        path_to_ds.mkdir(parents=True, exist_ok=True)
        dataset_name = PriceStore.get_dataset_name(start=start, end=end)
        pq.write_to_dataset(table, path_to_ds / dataset_name)

    @staticmethod
    def get_dataset_name(*, start: pd.Timestamp, end: pd.Timestamp):
        return f"{start.isoformat()}_{end.isoformat()}.parquet"

    def list_vendors(self):
        price_root = self._price_path
        return [VendorStore(price_root / Path(v)) for v in os.listdir(self._price_path)]

    def __repr__(self):
        return self.__str__().split("/")[-1]

    def __str__(self):
        return f"{self._price_path}"


class GsPriceStore(PriceStore):
    """
    Google Storage Price Store
    """

    def __init__(self, bucket_name: str, path_to_price_store: str):
        super().__init__(path_to_price_store)
        if path_to_price_store.startswith("/"):
            raise ValueError(
                f"{path_to_price_store} cannot start with / for Google Storage"
            )
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket_name)

    @staticmethod
    def _save_table(path_to_ds: str, table, start: pd.Timestamp, end: pd.Timestamp):
        raise NotImplementedError()

    def path_exists(self):
        blobs = self.bucket.list_blobs(prefix=str(self._price_path), max_results=1)
        for _ in blobs:
            return True

        return False

    def load_prices(
        self,
        *,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
        frequency: str,
    ) -> pa.Table:
        # sourcery skip: inline-immediately-returned-variable
        """
            Load prices from storage from start and end if exist
        :return:
        """
        if start is not None and end is not None:
            assert start < end
        if not self.path_exists():
            raise ValueError(f"{self._price_path} does not exist")

        # Note: we can update this later to add filtering
        price_store = self.get_ohclv_price_store_path(frequency=frequency)

        if start and end:
            price_dataset_name = PriceStore.get_dataset_name(start=start, end=end)
            return self.load_table(price_dataset_name, price_store, OHCL)
        else:
            return pq.read_table(
                f"gs://{self.bucket.name}/{self._price_path}", schema=OHCL
            )
