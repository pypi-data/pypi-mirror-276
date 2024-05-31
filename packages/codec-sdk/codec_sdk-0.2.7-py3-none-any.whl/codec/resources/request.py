from codec.constants import BASE_URL, TIMEOUT_MESSAGE, REQUEST_TIMEOUT
from requests.exceptions import ReadTimeout
from codec.exceptions import error_handler
import requests


class Request:
    def __init__(self, auth):
        self.auth = auth

    def _error_handler(self, error_code, error_message):
        error_handler(
            error_code=error_code,
            error_message=error_message
        )
    
    def get(self, endpoint, params=None):
        parameters = {}

        if params:
            parameters = {**params}
        
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", params=parameters, auth=self.auth, timeout=REQUEST_TIMEOUT)
            status_code = response.status_code
            response = response.json()
        except ReadTimeout:
            return self._error_handler(
                error_code="gateway_timeout",
                error_message=TIMEOUT_MESSAGE
            )
        
        if status_code != 200:
            return self._error_handler(
                error_code=response.get("detail").get("code"),
                error_message=response.get("detail").get("detail")
            )

        return response
    
    def post(self, endpoint, body=None, params=None):
        parameters = {}

        if params:
            parameters = {**params}

        if not body:
            body = {}

        try:
            response = requests.post(f"{BASE_URL}{endpoint}", json=body, params=parameters, auth=self.auth, timeout=REQUEST_TIMEOUT)
            status_code = response.status_code
            response = response.json()
        except ReadTimeout:
            return self._error_handler(
                error_code="gateway_timeout",
                error_message=TIMEOUT_MESSAGE
            )
        
        if status_code != 200:
            return self._error_handler(
                error_code=response.get("detail").get("code"),
                error_message=response.get("detail").get("detail")
            )

        return response

    def delete(self, endpoint, params=None):
        parameters = {}

        if params:
            parameters = {**params}
        
        try:
            response = requests.delete(f"{BASE_URL}{endpoint}", params=parameters, auth=self.auth, timeout=REQUEST_TIMEOUT)
            status_code = response.status_code
            response = response.json()
        except ReadTimeout:
            return self._error_handler(
                error_code="gateway_timeout",
                error_message=TIMEOUT_MESSAGE
            )
        
        if status_code != 200:
            return self._error_handler(
                error_code=response.get("detail").get("code"),
                error_message=response.get("detail").get("detail")
            )
        
        return response
