import os
from pathlib import Path
from typing import Optional, List

import pyarrow as pa
import pyarrow.parquet as pq

from finclaw.config import logger
from finclaw.data_store.storage_clients.StoreClient import StoreClient


class LocalStoreClient(StoreClient):
    """
    AWS S3 price store
    """

    def __init__(self):
        pass

    @staticmethod
    def _save_table(table: pa.Table, path: str):
        raise NotImplementedError()

    def listdir(self, path: str) -> List[str]:
        """
        Acts in a similar way to os.listdir
        Examples:
        os.listdir("/home")
        >> ['user1', 'user2', 'user3']
        Parameters
        ----------
        path - Path to the directory to list contents of
        Returns
        -------
            List of file names
        """
        return os.listdir(path)

    def path_exists(self, path: str) -> bool:
        """
        Check if path_to_price_store exists.
        Returns
        -------
            Boolean
        """
        return os.path.exists(path)

    def load_table(self, path: Path, schema: Optional[pa.Schema] = None):
        path = str(path)
        dataset = pq.ParquetDataset(path)
        table: pa.Table = dataset.read()
        return table

    def write_table(self, table: pa.Table, path: str | Path):
        if isinstance(path, Path):
            path = path.as_posix()
        logger.debug(f"Writing table to {path}")
        logger.debug(f"Table schema: {table.schema}")
        pq.write_to_dataset(table, path)
        logger.debug(f"{list(os.listdir(path))}")
