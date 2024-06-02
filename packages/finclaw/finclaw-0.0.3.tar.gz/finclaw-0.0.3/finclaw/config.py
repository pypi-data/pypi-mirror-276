import logging
import os

from pydantic import BaseSettings
from dotenv import load_dotenv

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def is_running_in_jupyter():
    try:
        # get_ipython is defined when this is called from inside Jupyter
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter Notebook
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type, assume not a Jupyter Notebook
    except NameError:
        return False  # Probably standard Python interpreter


class Settings(BaseSettings):
    TRADE_ENGINE_DATA: str
    FINNHUB_API: str = ""
    FINNHUB_STORAGE: str = "./finnhub_storage/daily"

    # FMP creds
    FMP_API_KEY: str = ""

    # TwelveData creds
    TWELVEDATA_API_KEY: str = ""

    # Kraken creds
    KRAKEN_API_KEY: str
    KRAKEN_API_SECRET: str
    USE_TQDM: bool = False

    # It can be set when using AWS
    S3_BUCKET_NAME: str = ""


if is_running_in_jupyter():
    logger.info("Running inside Jupyter")
    logger.info("Note that .env file should be in the same directory as this notebook")
    load_dotenv()
    settings = Settings()
else:
    load_dotenv()
    settings = Settings()
