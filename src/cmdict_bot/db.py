"""Function to query a word from the database."""
from cmdict.ecdict_connector import ECDICTConnector


def query_definitions(word: str) -> str:
    """Query the word in database.

    Args:
        word: English word to be queried.

    Returns:
        Definitions of the word.
    """
    db_engine = ECDICTConnector()
    return db_engine.query(word)["definition"]
