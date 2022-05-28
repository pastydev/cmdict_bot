
import os
from importlib.util import find_spec
import pathlib
import zipfile

from cmdict.ecdict_connector import ECDICTConnector
from loguru import logger as _LOG
import requests
from telegram import ForceReply, Update
from telegram.ext import Application, CallbackContext, CommandHandler, MessageHandler, filters

_TOKEN: str = os.environ.get('CMDICT_BOT')
_DB_URL = "https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip"  # noqa: E501


_db_dir = os.path.join(str(pathlib.Path(find_spec("cmdict").origin).parent), "data")
_db_file = os.path.join(_db_dir, "stardict.db")
_db_path = pathlib.Path(_db_file)
_db_zip = os.path.join(_db_dir, "stardict.zip")


def _download_stardict():
    data_dir_path = pathlib.Path(_db_dir)
    if not data_dir_path.exists():
        data_dir_path.mkdir(parents=True)

    r = requests.get(_DB_URL, stream=True)
    block_size = 1024

    _LOG.info("Start to download \"stardict.zip\" in {path}.", path=_db_zip)

    with open(_db_zip, "wb") as f:
        for data in r.iter_content(block_size):
            f.write(data)

    with zipfile.ZipFile(_db_zip, "r") as ref:
        ref.extractall(_db_dir)

    _LOG.success("\"stardict.zip\" has been downloaded and extracted.")


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    _LOG.info("New user: \"{name}\".", name=user.name)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def _query(word: str) -> str:
    db_engine = ECDICTConnector()
    return db_engine.query(word)['definition']


async def search(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    _LOG.debug("To echo a message sent by a user.")
    await update.message.reply_text(
        f"Definitions of \"{update.message.text}\" are: \n\n"
        + _query(update.message.text)
    )


def _start_app():
    _LOG.info("Telegram bot is being started.")

    # Create the Application and pass it your bot's token.
    app = Application.builder().token(_TOKEN).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    # Run the bot until the admin presses Ctrl-C
    app.run_polling()


def main() -> None:
    if not _db_path.is_file():
        _download_stardict()

    _start_app()


if __name__ == "__main__":
    main()
