"""Download ``stardict.db``, as required by ``cmdict``."""
from os import path

from importlib.util import find_spec
import pathlib
import zipfile

from cmdict.ecdict_connector import ECDICTConnector
from cmdict_bot.log import LOG
import requests

_DB_URL = "https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip"  # noqa: E501


_db_dir = path.join(str(pathlib.Path(find_spec("cmdict").origin).parent), "data")
_db_file = path.join(_db_dir, "stardict.db")
db_path = pathlib.Path(_db_file)
_db_zip = path.join(_db_dir, "stardict.zip")


def download_stardict():
    data_dir_path = pathlib.Path(_db_dir)
    if not data_dir_path.exists():
        data_dir_path.mkdir(parents=True)

    r = requests.get(_DB_URL, stream=True)
    block_size = 1024

    LOG.info("Start to download \"stardict.zip\" in {path}.", path=_db_zip)

    with open(_db_zip, "wb") as f:
        for data in r.iter_content(block_size):
            f.write(data)

    with zipfile.ZipFile(_db_zip, "r") as ref:
        ref.extractall(_db_dir)

    LOG.success("\"stardict.zip\" has been downloaded and extracted.")



def query(word: str) -> str:
    db_engine = ECDICTConnector()
    return db_engine.query(word)['definition']
