from pathlib import Path
from typing import Optional

import pandas as pd
import pyarrow as pa

from finclaw.config import logger
from finclaw.data_store.schema import OHCL
from finclaw.data_store.storage_clients.StoreClient import StoreClient


class PriceStoreV2:
    def __init__(
        self,
        path_to_price_store: str,
        storage_client: StoreClient,
        vendor: Optional[str] = None,
    ):
        self._price_path: Path = Path(path_to_price_store)
        if vendor:
            self._price_path = self._price_path / Path(vendor)
        self._storage_client = storage_client

    def list_datasets(self):
        if self._storage_client.path_exists(self._price_path):
            return self._storage_client.listdir(self._price_path)
        else:
            raise ValueError(f"price_path: {self._price_path} does not exit")

    # Loading logic
    def load_prices(
        self,
        *,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
        frequency: str,
    ) -> pa.Table:
        """
            Load prices from storage from start and end if exist
        :return:
        """
        if start is not None and end is not None:
            assert start < end
        self.path_exists()

        # Note: we can update this later to add filtering
        path_to_ohclv_store = self.get_ohclv_price_store_path(frequency=frequency)

        if start and end:
            price_dataset_name = PriceStoreV2.get_dataset_name(start=start, end=end)
            return self.load_table(price_dataset_name, path_to_ohclv_store, schema=OHCL)
        else:
            tables = []
            for table_name in self._storage_client.listdir(path_to_ohclv_store):
                table_for_one_freq = self.load_table(
                    table_name, path_to_ohclv_store, schema=OHCL
                )
                tables.append(table_for_one_freq)
            return pa.concat_tables(tables)

    def load_table(self, price_dataset, price_store, *, schema: pa.Schema) -> pa.Table:
        price_path = price_store / price_dataset
        if not self._storage_client.path_exists(price_path):
            raise ValueError(f"{price_path} does not exist")

        table = self._storage_client.load_table(price_path, schema=schema)
        return table

    def load_symbols(
        self,
        *,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> pa.Table:
        if start and end and start < end:
            raise ValueError(f"{start} should be smaller than {end}")
        self.path_exists()

        # Note: we can update this later to add filtering
        symbol_store_path = self.get_symbol_store_path()
        if start and end:
            symbol_dataset = PriceStoreV2.get_dataset_name(start=start, end=end)

            symbol_path = symbol_store_path / symbol_dataset
        else:
            symbol_path = symbol_store_path

        if not self._storage_client.path_exists(symbol_path):
            raise ValueError(f"{symbol_path} does not exist")

        table = self._storage_client.load_table(symbol_path)

        return table

    def load_financials(self, statement_type: str):
        self.path_exists()

        financial_store_path = self.get_financial_statement_store_path(
            statement_type=statement_type
        )
        table = self._storage_client.load_table(financial_store_path)
        return table

    def load_insiders(self, vendor):
        self.path_exists()

        insider_store_path = self.get_insider_store_path()
        return self._storage_client.load_table(insider_store_path)

    def path_exists(self):
        if not self._storage_client.path_exists(self._price_path):
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
            end=end, frequency=frequency, price_table=price_table, start=start
        )
        self.store_symbols(symbol_table=symbol_table, start=start, end=end)
        if company_table:
            self.store_company_descriptions(
                company_table=company_table, start=start, end=end
            )

    def store_prices(self, *, end, frequency, price_table, start):
        price_store_ds = self.get_ohclv_price_store_path(frequency)
        self._save_table(price_store_ds, price_table, start, end)

    def store_symbols(self, *, symbol_table, start: pd.Timestamp, end: pd.Timestamp):
        symbol_store_ds = self.get_symbol_store_path()
        self._save_table(symbol_store_ds, symbol_table, start, end)

    def store_company_descriptions(self, *, company_table, start, end):
        company_descriptions = self.get_company_descriptions()
        self._save_table(company_descriptions, company_table, start, end)

    def store_ownership(
        self,
        *,
        institutional_ownership_table: pa.Table,
        fund_ownership_table: pa.Table,
        all_owners_table: pa.Table,
        start,
        end,
    ):
        fund_ownership_path = self.get_ownership_store_path("fund")
        self._save_table(fund_ownership_path, fund_ownership_table, start, end)

        institutional_ownership_path = self.get_ownership_store_path("institutional")
        self._save_table(
            institutional_ownership_path, institutional_ownership_table, start, end
        )

        all_owners_path = self.get_ownership_store_path("all_owners")
        self._save_table(all_owners_path, all_owners_table, start, end)

    def store_insider_information(self, *, insider_table, start, end):
        insider_store_path = self.get_insider_store_path()
        self._save_table(insider_store_path, insider_table, start, end)

    def store_dividends(self, *, dividend_table, start, end):
        dividend_store_path = self.get_dividend_store_path()
        self._save_table(dividend_store_path, dividend_table, start, end)

    def store_financials(self, statement, financials_table, start, end, vendor):
        statement_store_path = self.get_financial_statement_store_path(
            vendor, statement
        )
        self._save_table(statement_store_path, financials_table, start, end)

    def store_splits(self, split_table, start, end):
        split_store_path = self.get_split_store_path()
        self._save_table(split_store_path, split_table, start, end)

    def get_symbol_store_path(self):
        return self._price_path / "symbols"

    def get_company_descriptions(self):
        return self._price_path / "company_descriptions"

    def get_ohclv_price_store_path(self, frequency):
        return self._price_path / "ohclv" / f"frequency_{frequency}"

    def get_ownership_store_path(self, ownership_type):
        return self._price_path / "ownership" / ownership_type

    def get_insider_store_path(self):
        return self._price_path / "insider"

    def get_dividend_store_path(self):
        return self._price_path / "dividends"

    def get_financial_statement_store_path(self, statement_type):
        return self._price_path / statement_type

    def get_split_store_path(self):
        return self._price_path / "splits"

    def _save_table(
        self, path_to_ds: Path, table, start: pd.Timestamp, end: pd.Timestamp
    ):
        self._storage_client.mkdir(path_to_ds, parents=True, exist_ok=True)
        dataset_name = PriceStoreV2.get_dataset_name(start=start, end=end)
        logger.debug(f"Writing table to {path_to_ds / dataset_name}")
        self._storage_client.write_table(table, path_to_ds / dataset_name)

    @staticmethod
    def get_dataset_name(*, start: pd.Timestamp, end: pd.Timestamp):
        return f"{start.isoformat()}_{end.isoformat()}.parquet"

    def list_vendors(self):
        # price_root = self._price_path
        # return [VendorStore(price_root / Path(v)) for v in os.listdir(self._price_path)]
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__().split("/")[-1]

    def __str__(self):
        return f"{self._price_path}"
