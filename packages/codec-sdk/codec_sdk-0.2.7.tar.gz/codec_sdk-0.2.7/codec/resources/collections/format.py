from codec.resources.collections.types import Collection
from codec.utils.type_utils import is_list_of_dicts
from codec.resources.videos.types import Video


def format_collection_object(collection_object):
    if is_list_of_dicts(collection_object.get("videos")):
        collection_object["videos"] = [Video(**video) for video in collection_object["videos"]]
    
    collection_object = Collection(**collection_object)

    return collection_object
