from codec.resources.collections.types import Collection
from codec.resources.videos.types import Video


def format_video_object(video_object):
    if isinstance(video_object.get("collection"), dict):
        video_object["collection"] = Collection(**video_object["collection"])

    video_object = Video(**video_object)

    return video_object
