"""File to be run for the app to start."""
from cmdict_bot.db import db_path, download_stardict
from cmdict_bot.app import start_bot


def main() -> None:
    if not db_path.is_file():
        download_stardict()

    start_bot()


if __name__ == "__main__":
    main()
