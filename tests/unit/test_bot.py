"""Test the Telegram bot."""
from os import environ

from cmdict_bot.bot import config_app

_TOKEN: str = environ.get("CMDICT_TEST_BOT")


def test_start_bot():
    """Test if the bot can be started correctly."""
    config_app(_TOKEN)
