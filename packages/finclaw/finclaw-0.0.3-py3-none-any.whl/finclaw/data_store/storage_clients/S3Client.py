from pathlib import Path
from typing import Optional, List

from pyarrow import fs
import pyarrow as pa
import pyarrow.parquet as pq

from finclaw.data_store.storage_clients.StoreClient import StoreClient
from finclaw.config import logger


class S3StoreClient(StoreClient):
    """
    AWS S3 price store
    """

    def __init__(self, bucket_name: str, region: str):
        if not bucket_name:
            raise ValueError("Bucket name should not be empty")

        self._s3_fs = fs.S3FileSystem(region=region)
        self._bucket_name = bucket_name

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
        try:
            files = self._s3_fs.get_file_info(
                fs.FileSelector(f"{self._bucket_name}/{path}")
            )
            return [f.base_name for f in files]
        except Exception as e:
            logger.exception(
                f"Exception while listing {self._bucket_name} / {path} we got {e}"
            )
            return []

    def path_exists(self, path: str) -> bool:
        """
        Check if path_to_price_store exists.
        Returns
        -------
            Boolean
        """
        file_path = f"{self._bucket_name}/{path}"
        result = self._s3_fs.get_file_info(file_path)
        return result.type != fs.FileType.NotFound

    def load_table(self, path: Path, schema: Optional[pa.Schema] = None):
        path = str(Path(self._bucket_name) / path)
        path = str(path)
        dataset = pq.ParquetDataset(
            path, use_legacy_dataset=False, schema=schema, filesystem=self._s3_fs
        )
        table: pa.Table = dataset.read()
        return table

    def write_table(self, table: pa.Table, path: str | Path):
        if isinstance(path, Path):
            path = path.as_posix()
        pq.write_to_dataset(
            table, f"{self._bucket_name}/{path}", filesystem=self._s3_fs
        )
