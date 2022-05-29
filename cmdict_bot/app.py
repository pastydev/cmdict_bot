"""Behaviors of the Telegram bot."""
from os import environ
from typing import Optional

from cmdict_bot.log import LOG
from cmdict_bot.db import query
from telegram import ForceReply, Update
from telegram.ext import Application, CallbackContext, CommandHandler, MessageHandler, filters

_TOKEN: str = environ.get('CMDICT_BOT')


async def _search(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    LOG.debug("To echo a message sent by a user.")
    await update.message.reply_text(
        f"Definitions of \"{update.message.text}\" are: \n\n"
        + query(update.message.text)
    )


async def _start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    LOG.info("New user: \"{name}\".", name=user.name)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def _help_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def start_bot(token: Optional[str] = _TOKEN):
    LOG.info("Telegram bot is being started.")

    # Create the Application and pass it your bot's token.
    bot = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    bot.add_handler(CommandHandler("start", _start))
    bot.add_handler(CommandHandler("help", _help_command))

    # on non command i.e message - echo the message on Telegram
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _search))

    # Run the bot until the admin presses Ctrl-C
    bot.run_polling()
