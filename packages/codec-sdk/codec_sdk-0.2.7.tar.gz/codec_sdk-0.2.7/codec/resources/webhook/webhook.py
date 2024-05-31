from svix.webhooks import WebhookVerificationError
from svix.webhooks import Webhook as SvixWebhook
from codec.exceptions import WebhookException
from typing import Union
import json


def _construct_event(
    payload,
    headers,
    secret
):
    if isinstance(headers, str):
        headers = json.loads(headers)
    elif isinstance(headers, dict):
        pass
    
    if isinstance(payload, dict):
        payload_formatted = json.dumps(payload, separators=(",", ":"))
    elif isinstance(payload, str):
        pass
    
    wh = SvixWebhook(secret)
    
    try:
        wh.verify(payload_formatted, headers)
    except WebhookVerificationError as e:
        raise WebhookException(str(e))

    return payload


class Webhook:
    def __init__(self, auth):
        self.auth = auth

    def construct_event(
        self,
        payload: Union[dict, str],
        headers: Union[dict, str],
        secret: str
    ):
        event = _construct_event(
            payload=payload,
            headers=headers,
            secret=secret
            
        )

        return event
