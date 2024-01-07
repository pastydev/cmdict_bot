"""Functions related to database."""
from importlib.util import find_spec
from os import path
from pathlib import Path
from zipfile import ZipFile

from cmdict.ecdict_connector import ECDICTConnector
from requests import get

from cmdict_bot.log import LOG

_URL = "https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip"  # noqa: E501
_DIR = path.join(str(Path(find_spec("cmdict").origin).parent), "data")
_DB_PATH = Path(path.join(_DIR, "stardict.db"))
_ZIP_PATH = path.join(_DIR, "stardict.zip")


def get_stardict():
    """Download and extract `stardict.db` to `data` dir of cmdict."""
    data_dir_path = Path(_DIR)
    if not data_dir_path.exists():
        data_dir_path.mkdir(parents=True)

    r = get(_URL, stream=True)
    block_size = 1024

    LOG.info('Start to download "stardict.zip" in {path}.', path=_ZIP_PATH)

    with open(_ZIP_PATH, "wb") as f:
        for data in r.iter_content(block_size):
            f.write(data)

    with ZipFile(_ZIP_PATH, "r") as ref:
        ref.extractall(_DIR)

    LOG.success(
        f'"stardict.zip" has been downloaded and extracted to {_DB_PATH}.'
    )


def query_definitions(word: str) -> str:
    """Query the word in database.

    Args:
        word: English word to be queried.

    Returns:
        Definitions of the word.
    """
    db_engine = ECDICTConnector()
    return db_engine.query(word)["definition"]
