"""Main file of the serverless application."""
import asyncio

from cmdict_bot.bot import run


def lambda_handler(event, context):
    """Set AWS Lambda entry point to handles HTTP request from API Gateway."""
    return asyncio.get_event_loop().run_until_complete(run(event, context))
