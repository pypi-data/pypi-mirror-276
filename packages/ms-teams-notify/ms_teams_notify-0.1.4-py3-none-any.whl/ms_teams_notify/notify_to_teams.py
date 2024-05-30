import logging
from urllib.parse import urlparse

import requests


def _get_hostname_from_url(url: str):
    parsed_url = urlparse(url)
    return parsed_url.hostname


def _assemble_request_json(
    title: str,
    messages: list[str] = None,
    urls: list[str] = None,
):
    body = [{
        "type": "TextBlock",
        "size": "large",
        "weight": "bolder",
        "text": title,
        "wrap": True,
    }]

    body += [{
        "type": "TextBlock",
        "size": "default",
        "weight": "default",
        "text": message,
        "wrap": True,
    } for message in messages] if messages else []

    actions = [{
        "type": "Action.OpenUrl",
        "title": _get_hostname_from_url(url),
        "url": url,
        "wrap": True,
    } for url in urls] if urls else []

    request_json = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.6",
                    "body": body,
                    "actions": actions,
                }
            }
        ]
    }

    logging.debug(request_json)

    return request_json


def notify_to_teams(
    webhook_url: str,
    title: str,
    messages: list[str] = None,
    urls: list[str] = None,
):
    request_json = _assemble_request_json(
        title=title,
        messages=messages,
        urls=urls,
    )

    response = requests.post(
        url=webhook_url,
        json=request_json,
        timeout=10,
    )

    logging.debug(response.status_code)
    logging.debug(response.text)

    return response
