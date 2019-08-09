#!/usr/bin/env python3
import click
import json
from learnosity_sdk.request import DataApi


def validate_endpoint(ctx, param, value) -> str:
    error_message = "Must be one of `activities`, `items`, or `questions`"
    if value in ["activities", "items", "questions"]:
        return value
    else:
        raise click.BadParameter(error_message)


def validate_credentials_file(filepath: str) -> dict:
    error_message = """
                    Sorry, but you have to supply a valid path to a JSON file
                    with your Learnosity credentials. See --help for more info
                    """
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            credentials: dict = json.load(f)
            return credentials
    except (FileNotFoundError, TypeError, json.decoder.JSONDecodeError):
        raise click.BadParameter(error_message)


def validate_credentials(ctx, param, value):
    credentials: dict = validate_credentials_file(value)
    error_message = """
                    Sorry, your credentials JSON doesn't seem to match the spec.
                    See --help for more details
                    """

    if all(
        k in credentials.keys()
        for k in ("consumerKey", "consumerSecret", "domain")
    ):
        return credentials
    else:
        raise click.BadParameter(error_message)


def make_request_packet(reference: str, limit: str):
    if reference is None:
        return {"limit": limit}
    else:
        return {"references": [reference]}


def get_response_from_api(
    endpoint: str, reference_id: str, credentials: dict, limit: str
):
    api_url: str = "".join(
        ["https://data.learnosity.com/v1/itembank/", endpoint]
    )
    client = DataApi()
    response = client.request(
        endpoint=api_url,
        security_packet={
            "consumer_key": credentials["consumerKey"],
            "domain": credentials["domain"],
        },
        secret=credentials["consumerSecret"],
        request_packet=make_request_packet(reference_id, limit),
        action="get",
    )

    return json.dumps(response.json(), indent=2)


@click.command()
@click.option(
    "--endpoint",
    type=click.Choice(["activities", "items", "questions"]),
    help="""
         The Learnosity API Endpoint you'd like to use. Must be one of `activities`, `items`, or `questions`
         """,
    callback=validate_endpoint,
)
@click.option(
    "--credentials",
    type=str,
    help="""
         The Path to a JSON file which has top-level keys for the Learnosity API: `consumerKey`, `consumerSecret`, and `domain`
         """,
    callback=validate_credentials,
)
@click.option(
    "--reference",
    default=None,
    help="""
         The reference ID of the Learnosity activity, item, or question you're looking for.
         """,
)
@click.option(
    "--limit",
    default=10,
    help="""
         The max number of responses to return.
         Only applies when no `reference` value is set.
         """,
)
def get_data_from_learnosity(
    endpoint: str, reference: str, credentials: dict, limit: str
):
    """
    A simple script to grab data (activities, items, and/or questions) from a Learnosity item bank. This script sends its JSON output to `stdout`, but you can redirect that output to a file of your choosing :-)
    """

    output = get_response_from_api(endpoint, reference, credentials, limit)
    click.echo(output)


if __name__ == "__main__":
    get_data_from_learnosity()
