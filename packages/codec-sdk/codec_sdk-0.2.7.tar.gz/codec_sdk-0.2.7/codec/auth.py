from requests.auth import AuthBase
from codec.constants import CLIENT


class CodecAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        request.headers.update({
            "Content-Type": "Application/JSON",
            "User-Agent": CLIENT,
            "Authorization": self.api_key
        })

        return request
