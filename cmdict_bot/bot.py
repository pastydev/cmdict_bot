"""Commands and non-command behaviour of the Telegram bot."""
from os import environ
from os import path
from pathlib import Path
from typing import Optional

from telegram import Update
from telegram.ext import Application
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import filters
from telegram.ext import MessageHandler

from cmdict_bot.db import query_definitions
from cmdict_bot.log import LOG

#: Token of the bot for production.
_TOKEN: str = environ.get("CMDICT_BOT")

_path = path.join(str(Path(__file__).parent.parent), "README.md")
_START: str = open(_path, "r").read()


async def _search(
    update: Update, context: CallbackContext.DEFAULT_TYPE
) -> None:
    """Search user-input.

    Args:
        update: sent from the user.
        context: more info on the user.
    """
    LOG.debug("To echo a message sent by a user.")
    await update.message.reply_text(
        f'Definitions of "{update.message.text}" are: \n\n'
        + query_definitions(update.message.text)
    )


async def _start(
    update: Update, context: CallbackContext.DEFAULT_TYPE
) -> None:
    """Send a message to first-time user.

    Args:
        update: sent from the user.
        context: more info on the user.
    """
    user = update.effective_user
    LOG.info(
        'New user: "{user_name}" has started the bot.', user_name=user.name
    )

    await update.message.reply_markdown(_START)


async def _help_command(
    update: Update, context: CallbackContext.DEFAULT_TYPE
) -> None:
    """Send a message when the command /help is issued.

    Args:
        update: sent from the user.
        context: more info on the user.
    """
    await update.message.reply_text("Help!")


def start_bot(token: Optional[str] = _TOKEN):
    """Start a Telegram bot for a token.

    Args:
        token: token of the Telegram bot. Default to be the token of the
            bot for production. The token of the bot for testing can be
            passed. The token is stored as an environment variable.
    """
    LOG.info("The Telegram bot is being started.")

    # Create the Application and pass it your bot's token.
    bot = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    bot.add_handler(CommandHandler("start", _start))
    bot.add_handler(CommandHandler("help", _help_command))

    # on non command i.e message - echo the message on Telegram
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _search))

    # Run the bot until the admin presses Ctrl-C
    bot.run_polling()
