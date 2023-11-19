"""Commands and non-command behaviour of the Telegram bot."""
import json
from os import environ
import traceback
from typing import Optional

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import filters
from telegram.ext import MessageHandler
from telegram.ext import ContextTypes

from .db import query_definitions
from .log import LOG

#: Token of the bot for production.
_TOKEN: str = environ.get("CMDICT_TEST_BOT")
# See supported HTML in https://core.telegram.org/bots/api#html-style.
#: Message sent to user at the start, formatted in HTML.
_START: str = """
<b>cmdict_bot</b>: "pasty-dev/cmdict" as Telegram bot.

Send it an English word and receive its definitions. For example, if you send "test", if will reply:

<i>Definitions of "test" are:

n. any standardized procedure for measuring sensitivity or memory or intelligence or aptitude or personality etc
n. the act of undergoing testing
n. the act of testing something
n. a hard outer covering as of some amoebas and sea urchins </i>

Check out the source code of "pasty-dev/cmdict" in https://github.com/pasty-dev/cmdict.
"""  # noqa: E501


async def _search(
    update: Update, context: ContextTypes.DEFAULT_TYPE
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
    update: Update, context: ContextTypes.DEFAULT_TYPE
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

    await update.message.reply_text(_START, parse_mode=ParseMode.HTML)


async def _help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a message when the command /help is issued.

    Args:
        update: sent from the user.
        context: more info on the user.
    """
    await update.message.reply_text("Help!")


def config_app(token: Optional[str] = _TOKEN) -> Application:
    """Config a Telegram bot.

    Args:
        token: _description_. Defaults to _TOKEN.

    Returns:
        Application: _description_
    """
    # Create the Application and pass it your bot's token.
    app = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", _start))
    app.add_handler(CommandHandler("help", _help_command))

    # on non command i.e message - echo the message on Telegram
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _search))
    
    return app


async def run(event: dict, context) -> dict:
    """Run Telegram bot.

    Args:
        event (dict): _description_
        context (_type_): _description_

    Returns:
        dict: _description_
    """
    value: dict
    try:
        jss = json.loads(event["body"])
        jss["update_id"] = 1 # Update.de_json expects update_id to be present, so as temporary workaround, we set it to 1. See this issue --> https://github.com/jojo786/Sample-Python-Telegram-Bot-AWS-Serverless-PTBv20/issues/1
        app = config_app()
        update = Update.de_json(jss, app.bot)
        app.process_update(update)
        value = {"statusCode": 200, "body": "Success"}
    except Exception as exc:
        traceback.print_exc()
        print(f"Error: {exc}")
        value = {"statusCode": 500, "body": f"Error: {exc}"}
    return value
