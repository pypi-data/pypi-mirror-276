import json
from random import random

import requests
from onchainpay_api.resources.constants import REQUEST_TIMEOUT_RESPONSE
from onchainpay_api.resources.response import FailResponse, SuccessResponse
from onchainpay_api.resources.utils import create_signature, format_response_error


class APIRequestor:
    def __init__(
            self,
            public_key: str,
            private_key: str,
            url: str,
            payload: dict = None
    ):
        self.url = url
        self.body = ""

        self.headers = {}
        self.payload = payload or {}

        self.set_nonce()
        self.set_auth_headers(public_key, private_key)

    def set_nonce(self):
        self.payload.update({"nonce": round(random() * 1000000000)})

    def set_auth_headers(self, public_key: str, secret: str):
        self.body = json.dumps(self.payload)

        self.headers.update(
            {
                "Content-Type": "application/json",
                "x-api-public-key": public_key,
                "x-api-signature": create_signature(secret, self.body),
            }
        )

    def post(self):
        try:
            response = requests.post(
                self.url,
                data=self.body,
                headers=self.headers,
            )
        except BaseException as e:
            return FailResponse(-1, e.args[1])

        try:
            return response.json()
        except json.JSONDecodeError:
            return format_response_error(response)
