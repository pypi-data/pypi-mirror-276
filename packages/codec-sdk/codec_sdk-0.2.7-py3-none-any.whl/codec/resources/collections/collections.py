from codec.resources.collections.format import format_collection_object
from codec.resources.request import Request


class Collections:
    def __init__(self, auth):
        self.auth = auth

    def create(
        self,
        name: str
    ):
        endpoint = "/collection"
        response = Request(self.auth).post(endpoint, body={"name": name})
        response = format_collection_object(response)
        
        return response
    
    def get(
        self,
        uid: str = None,
        expand: list = None
    ):
        if uid:
            endpoint = f"/collection/{uid}"
        else:
            endpoint = "/collection"
        
        expand_parameter = None if expand is None else {"expand": ",".join(expand)}
        response = Request(self.auth).get(endpoint, params=expand_parameter)
        
        if isinstance(response, dict):
            response = format_collection_object(response)
        elif isinstance(response, list):
            response = [format_collection_object(collection) for collection in response]

        return response
