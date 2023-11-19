import asyncio

from cmdict_bot.bot import run


def lambda_handler(event, context):
    """Set AWS Lambda entry point. Handles the HTTP request from API Gateway.

    Args:
        event: _description_
        context: _description_

    Returns:
        
    """
    return asyncio.get_event_loop().run_until_complete(run(event, context))
