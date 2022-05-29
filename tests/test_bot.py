"""Test the Telegram bot."""
from os import environ

from cmdict_bot.bot import start_bot

_TOKEN: str = environ.get("CMDICT_BOT")


def test_start_bot():
    """Test if the bot can be started correctly."""
    start_bot(_TOKEN)
