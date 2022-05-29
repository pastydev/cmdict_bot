from os import environ

from cmdict_bot.app import start_bot

_TOKEN: str = environ.get('CMDICT_BOT')


def test_start_bot():
    """Test if the bot can be started correctly."""
    start_bot(_TOKEN)
