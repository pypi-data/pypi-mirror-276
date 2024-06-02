import json

import requests

from kozmo_ai.server.logger import Logger
from kozmo_ai.services.slack.config import SlackConfig

logger = Logger().new_server_logger(__name__)


def send_slack_message(config: SlackConfig, message: str, title: str = None) -> None:
    message = message.replace('\\n', '\n')
    payload = {
        'blocks': [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': title if title else 'Kozmo Notification',
                },
            },
            {'type': 'divider'},
            {'type': 'section', 'text': {'type': 'mrkdwn', 'text': message}},
        ]
    }

    response = requests.post(
        config.webhook_url,
        json.dumps(payload),
    )

    try:
        if response is not None:
            response.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.exception('Failed to send slack message')
