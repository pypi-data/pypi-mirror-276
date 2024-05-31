from codec.resources.search.types import SearchResult
from codec.resources.request import Request


def search_with_query(
    query,
    auth,
    search_types,
    video,
    collection,
    max_results
) -> list[SearchResult]:
    endpoint = "/search"
    results = Request(auth).post(
        endpoint=endpoint,
        body={
            "query": query,
            "search_types": search_types,
            "video": video,
            "collection": collection,
            "max_results": max_results
        }
    )

    results = [SearchResult(**result) for result in results]

    return results
