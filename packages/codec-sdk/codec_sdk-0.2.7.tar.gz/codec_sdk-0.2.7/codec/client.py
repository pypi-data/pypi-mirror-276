from codec.resources import (
    Collections,
    Videos,
    Webhook
)
from codec.resources.search.search import search_with_query
from codec.auth import CodecAuth
from typing import List
import logging


# Disable httpx logs (supabase)
logging.getLogger("httpx").setLevel(logging.CRITICAL)


class Codec:
    def __init__(self, api_key: str):
        self.auth = CodecAuth(api_key=api_key)

    @property
    def collections(self):
        return Collections(self.auth)

    @property
    def videos(self):
        return Videos(self.auth)

    @property
    def webhook(self):
        return Webhook(self.auth)

    def search(
        self,
        query: str,
        search_types: List[str] = None,
        video: str = None,
        collection: str = None,
        max_results:int = 10
    ):
        results = search_with_query(
            query=query,
            auth=self.auth,
            search_types=search_types,
            video=video,
            collection=collection,
            max_results=max_results
        )

        return results
