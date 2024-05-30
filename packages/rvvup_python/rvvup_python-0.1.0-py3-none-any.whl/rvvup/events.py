from typing import Optional, Dict, Any


class Events:

    def __init__(self, client):
        self.client = client

    def create_event(
        self, event_type: str, reason: str, data: Optional[Dict[str, Any]] = None
    ) -> None:
        query = """
            mutation eventCreate($input: AuditLogCreateInput!) {
                eventCreate(input: $input) {
                    id
                }
            }
            """
        variables = {
            "input": {
                "actionType": event_type,
                "merchant": {
                    "id": self.client.merchant_id,
                },
                # The resource the event refers to (order, merchant etc)
                "resourceId": self.client.merchant_id,
                "reason": reason,
                "currentData": data or {},
            },
        }
        self.client.graphql(query, variables)
