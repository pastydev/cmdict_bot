"""Download ``stardict.db``, as required by ``cmdict``."""
from importlib.util import find_spec
from os import path
from pathlib import Path
from zipfile import ZipFile

from cmdict.ecdict_connector import ECDICTConnector
from requests import get

from cmdict_bot.log import LOG

_DB_URL = "https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip"  # noqa: E501


_DB_DIR = path.join(str(Path(find_spec("cmdict").origin).parent), "data")
_DB_PATH = Path(path.join(_DB_DIR, "stardict.db"))
_DB_ZIP = path.join(_DB_DIR, "stardict.zip")


def get_stardict():
    """Download and extract ``stardict.db``."""
    data_dir_path = Path(_DB_DIR)
    if not data_dir_path.exists():
        data_dir_path.mkdir(parents=True)

    r = get(_DB_URL, stream=True)
    block_size = 1024

    LOG.info('Start to download "stardict.zip" in {path}.', path=_DB_ZIP)

    with open(_DB_ZIP, "wb") as f:
        for data in r.iter_content(block_size):
            f.write(data)

    with ZipFile(_DB_ZIP, "r") as ref:
        ref.extractall(_DB_DIR)

    LOG.success('"stardict.zip" has been downloaded and extracted.')


def query_definitions(word: str) -> str:
    """Query the word in database.

    Args:
        word: English word to be queried.

    Returns:
        Definitions of the word.
    """
    if not _DB_PATH.exists():
        get_stardict()

    db_engine = ECDICTConnector()
    return db_engine.query(word)["definition"]
