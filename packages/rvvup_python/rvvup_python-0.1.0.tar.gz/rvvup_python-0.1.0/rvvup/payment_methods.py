from typing import Optional, Dict, Any, List


class PaymentMethods:

    def __init__(self, client):
        self.client = client

    def get_available_payment_methods(
        self,
        cart_total: Optional[str] = None,
        currency: Optional[str] = None,
        input_options: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        query = """
            query merchant ($id: ID!, $total: MoneyInput) {
                merchant (id: $id) {
                    paymentMethods (search: {includeInactive: false, total: $total}) {
                        edges {
                            node {
                                name
                                displayName
                                description
                                summaryUrl
                                assets {
                                    assetType
                                    url
                                    attributes
                                }
                                limits {
                                    total {
                                        min
                                        max
                                        currency
                                    }
                                    expiresAt
                                }
                                settings {
                                    assets {
                                        assetType
                                        url
                                        attributes
                                    }
                                    ... on PaypalPaymentMethodSettings {
                                        checkout {
                                            button {
                                                enabled
                                                layout {
                                                    value
                                                }
                                                color {
                                                    value
                                                }
                                                shape {
                                                    value
                                                }
                                                label {
                                                    value
                                                }
                                                tagline
                                                size
                                            }
                                            payLaterMessaging {
                                                enabled
                                                layout {
                                                    value
                                                }
                                                logoType {
                                                    value
                                                }
                                                logoPosition {
                                                    value
                                                }
                                                textColor {
                                                    value
                                                }
                                                textSize
                                                textAlignment {
                                                    value
                                                }
                                                color {
                                                    value
                                                }
                                                ratio {
                                                    value
                                                }
                                            }
                                        }
                                        product {
                                            button {
                                                enabled
                                                layout {
                                                    value
                                                }
                                                color {
                                                    value
                                                }
                                                shape {
                                                    value
                                                }
                                                label {
                                                    value
                                                }
                                                tagline
                                                size
                                            }
                                            payLaterMessaging {
                                                enabled
                                                layout {
                                                    value
                                                }
                                                logoType {
                                                    value
                                                }
                                                logoPosition {
                                                    value
                                                }
                                                textColor {
                                                    value
                                                }
                                                textSize
                                                textAlignment {
                                                    value
                                                }
                                                color {
                                                    value
                                                }
                                                ratio {
                                                    value
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """

        total = None
        if cart_total and currency:
            total = {
                "amount": cart_total,
                "currency": currency,
            }

        variables = {
            "id": self.client.merchant_id,
            "total": total,
        }

        try:
            response = self.client.graphql(query, variables, input_options)
        except Exception as e:
            self.client.log("Could not complete request {error}", {"error": str(e)})
            return []

        response_methods = (
            response.get("data", {})
            .get("merchant", {})
            .get("paymentMethods", {})
            .get("edges", [])
        )
        methods = []
        for response_method in response_methods:
            method = response_method["node"]
            methods.append(
                {
                    "name": method["name"],
                    "displayName": method["displayName"],
                    "description": method["description"],
                    "summaryUrl": method["summaryUrl"],
                    "assets": method["assets"],
                    "limits": method["limits"],
                    "settings": method.get("settings"),
                }
            )

        return methods
