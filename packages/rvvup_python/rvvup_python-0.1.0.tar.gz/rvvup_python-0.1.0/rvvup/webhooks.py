import json
from typing import Dict, Any

from openapi.rvvup.api.webhooks import (
    list_webhooks,
    create_webhook,
    update_webhook,
    get_webhook,
)
from openapi.rvvup.models import (
    WebhookCreateInput,
    WebhookUpdateInput,
    WebhookEventType,
    WebhookStatus,
)


class Webhooks:

    def __init__(self, client):
        self.client = client

    def find(self):
        result = list_webhooks.sync_detailed(
            self.client.merchant_id, client=self.client.httpx_client()
        )
        return json.loads(result.content)

    def get(self, webhook_id: str):
        result = get_webhook.sync_detailed(
            self.client.merchant_id, webhook_id, client=self.client.httpx_client()
        )
        return json.loads(result.content)

    def create(
        self, url: str, subscribed_events: list[WebhookEventType], headers=None
    ) -> Dict[str, Any]:

        if headers is None:
            headers = {}

        webhook = WebhookCreateInput(
            headers=headers,
            subscribed_events=subscribed_events,
            url=url,
        )
        result = create_webhook.sync_detailed(
            self.client.merchant_id,
            client=self.client.httpx_client(),
            body=webhook,
        )
        return json.loads(result.content)

    def update(
        self,
        webhook_id: str,
        url: str,
        subscribed_events: list[WebhookEventType],
        status: WebhookStatus,
        headers=None,
    ) -> Dict[str, Any]:

        if headers is None:
            headers = {}

        webhook = WebhookUpdateInput(
            url=url,
            headers=headers,
            subscribed_events=subscribed_events,
            status=status,
        )

        result = update_webhook.sync_detailed(
            self.client.merchant_id,
            webhook_id,
            client=self.client.httpx_client(),
            body=webhook,
        )
        return json.loads(result.content)
