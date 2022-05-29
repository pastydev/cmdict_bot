"""File to be run for the bot to start."""
from cmdict_bot.bot import start_bot
from cmdict_bot.db import db_path
from cmdict_bot.db import get_stardict


def main() -> None:
    """Get ``stardict.db`` and start the bot for production."""
    if not db_path.is_file():
        get_stardict()

    start_bot()


if __name__ == "__main__":
    main()
