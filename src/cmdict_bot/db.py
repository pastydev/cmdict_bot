"""Function to query a word from the database."""
from cmdict.ecdict_connector import ECDICTConnector
from cmdict_bot.log import LOG


def query_definitions(word: str) -> str:
    """Query the word in database.

    Args:
        word: English word to be queried.

    Returns:
        Definitions of the word.
    """
    LOG.debug(f'To query "{word}".')
    db_engine = ECDICTConnector()
    return db_engine.query(word)["definition"]
