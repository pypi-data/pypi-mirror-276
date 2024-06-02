from tqdm import tqdm
from finclaw.config import settings, logger


def simple_progress_bar(iterable, desc: str = None):
    counter = 0
    for i in iterable:
        if counter % 55 == 0:
            if desc:
                logger.info(counter)
            else:
                logger.info(f"{desc}:{counter}")
        counter += 1
        yield i


def get_progress_bar(desc: str = None):
    if settings.USE_TQDM:
        if desc:
            return lambda x: tqdm(x, desc=desc)
        else:
            return lambda x: tqdm(x)
    else:
        if desc:
            return lambda itr: simple_progress_bar(itr, desc=desc)
        else:
            return simple_progress_bar


progress_bar = get_progress_bar()
