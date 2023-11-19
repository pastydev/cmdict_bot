import os

import boto3
import pytest
import requests

_REGION_NAME = "eu-central-1"
_STACK_NAME = "CmdictBot"


@pytest.fixture()
def api_gateway_url():
    """ Get the API Gateway URL from Cloudformation Stack outputs """
    client = boto3.client("cloudformation", region_name=_REGION_NAME)

    try:
        response = client.describe_stacks(StackName=_STACK_NAME)
    except Exception as e:
        raise Exception(
            f"Cannot find stack {_STACK_NAME} \n" f'Please make sure a stack with the name "{_STACK_NAME}" exists'
        ) from e

    stacks = response["Stacks"]
    stack_outputs = stacks[0]["Outputs"]
    api_outputs = [output for output in stack_outputs if output["OutputKey"] == "CmdictBotApi"]

    if not api_outputs:
        raise KeyError(f"CmdictBotApi not found in stack {_STACK_NAME}")

    return api_outputs[0]["OutputValue"]  # Extract url from stack outputs


def test_api_gateway(api_gateway_url):
    """ Call the API Gateway endpoint and check the response """
    response = requests.get(api_gateway_url)

    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}
