from typing import Dict, Any


class Orders:

    def __init__(self, client):
        self.client = client

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        query = """
            mutation OrderCreate($input: OrderCreateInput!) {
                orderCreate(input: $input) {
                    id
                    status
                    redirectToCheckoutUrl
                    dashboardUrl
                    paymentSummary {
                        paymentActions {
                            type
                            method
                            value
                        }
                    }
                }
            }
            """
        return self.client.graphql(query, order_data)

    def update_express_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        query = """
            mutation orderExpressUpdate ($input: OrderExpressUpdateInput!) {
                orderExpressUpdate(input: $input) {
                    id
                    type
                    externalReference
                    status
                    dashboardUrl
                    paymentSummary {
                        paymentActions {
                            type
                            method
                            value
                        }
                    }
                }
            }
            """
        response = self.client.graphql(query, order_data)
        return response.get("data", {}).get("orderExpressUpdate", {})

    def get_order(self, order_id: str) -> Dict[str, Any]:
        query = """
            query order ($id: ID!, $merchant: IdInput!) {
                order (id: $id, merchant: $merchant) {
                    id
                    type
                    externalReference
                    total {
                        amount
                        currency
                    }
                    redirectToStoreUrl
                    redirectToCheckoutUrl
                    status
                    dashboardUrl
                }
            }
            """
        variables = {
            "id": order_id,
            "merchant": {
                "id": self.client.merchant_id,
            },
        }

        response = self.client.graphql(query, variables)
        return response.get("data", {}).get("order", {})

    def is_order_refundable(self, order_id: str) -> bool:
        query = """
            query order ($id: ID!, $merchant: IdInput!) {
                order (id: $id, merchant: $merchant) {
                    paymentSummary {
                        isRefundable
                    }
                }
            }
            """
        variables = {
            "id": order_id,
            "merchant": {
                "id": self.client.merchant_id,
            },
        }
        response = self.client.graphql(query, variables)
        return (
            response.get("data", {})
            .get("order", {})
            .get("paymentSummary", {})
            .get("isRefundable", False)
        )

    def refund_order(
        self, order_id: str, amount: float, reason: str, idempotency: str
    ) -> Dict[str, Any]:
        query = """
            mutation orderRefund ($input: OrderRefundInput!) {
                orderRefund (input: $input) {
                    id
                    externalReference
                    payments {
                      refunds {
                        id
                        status
                        reason
                      }
                    }
                }
            }
            """
        variables = {
            "input": {
                "id": order_id,
                "merchant": {
                    "id": self.client.merchant_id,
                },
                "amount": {
                    "amount": amount,
                    "currency": "GBP",
                },
                "reason": reason,
                "idempotencyKey": idempotency,
            },
        }
        response = self.client.graphql(query, variables)
        return response.get("data", {}).get("orderRefund", {})

    def refund_create(self, input: Dict[str, Any]) -> Dict[str, Any]:
        query = """
            mutation refundCreate ($input: RefundCreateInput!) {
                refundCreate (input: $input) {
                    id
                    amount {
                        amount
                        currency
                    }
                    status
                }
            }
            """
        variables = {
            "input": {
                "orderId": input["orderId"],
                "merchantId": self.client.merchant_id,
                "amount": {
                    "amount": input["amount"],
                    "currency": input["currency"],
                },
                "reason": input["reason"],
                "idempotencyKey": input["idempotencyKey"],
            },
        }
        response = self.client.graphql(query, variables)
        return response.get("data", {}).get("refundCreate", {})

    def get_order_refunds(self, order_id: str) -> Dict[str, Any]:
        query = """
            query order ($id: ID!, $merchant: IdInput!) {
                order (id: $id, merchant: $merchant) {
                    id
                    payments {
                        id
                        refunds {
                            id
                            status
                            reason
                            amount {
                                amount
                                currency
                            }
                        }
                    }
                }
            }
            """
        variables = {
            "id": order_id,
            "merchant": {
                "id": self.client.merchant_id,
            },
        }
        response = self.client.graphql(query, variables)
        return response.get("data", {}).get("order", {}).get("payments", {})
