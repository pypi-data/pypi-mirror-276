from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional
import pyarrow as pa

class StoreClient(ABC):
    """
    Base StoreClient for storing pyarrow tables
    """

    @abstractmethod
    def listdir(self, path: str | Path) -> List[str]:
        pass

    @abstractmethod
    def path_exists(self, path: str | Path) -> bool:
        pass

    @abstractmethod
    def load_table(self, path: str | Path, schema: Optional[pa.Schema] = None):
        pass

    @abstractmethod
    def write_table(self, table: pa.Table, path: str | Path) -> None:
        pass

    def mkdir(self, path_to, parents, exist_ok):
        # on local fs it will be         path_to_ds.mkdir(parents=True, exist_ok=True)
        pass

