from codec.resources.videos.types import (
    VideoStatus,
    PreUploadedVideo
)
from codec.constants import SUPABASE_URL, SUPABASE_PUBLIC_KEY, POLLING_INTERVAL
from codec.utils.file_utils import validate_path_and_get_filename
from codec.resources.videos.format import format_video_object
from codec.resources.request import Request
from supabase import create_client
import time


supabase = create_client(
    supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_PUBLIC_KEY
)


def _upload_video(path, auth, collection):
    # Validate video path and get video filename
    filename = validate_path_and_get_filename(path)
    file_extension = filename.split(".")[-1]

    # Upload video
    pre_upload_endpoint = "/upload/pre"
    pre_upload_response = Request(auth).post(
        pre_upload_endpoint,
        body={
            "original_filename": filename,
            "collection": collection
        }
    )
    pre_upload_response = PreUploadedVideo(**pre_upload_response)

    with open(path, "rb") as f:
        supabase.storage.from_("codec-multi").upload_to_signed_url(
            path=pre_upload_response.path,
            token=pre_upload_response.token,
            file=f,
            file_options={
                "content-type": f"video/{file_extension}"
            }
        )

    return pre_upload_response


def _index_video(uid, auth, wait):
    # Queue indexing
    endpoint = f"/index/{uid}"
    response = Request(auth).post(endpoint)

    # Poll indexer status until indexed if wait is True
    if wait:
        keep_polling = True
        while keep_polling:
            response = Request(auth).get(endpoint)

            if response.get("status") == "indexed":
                keep_polling = False
            
            time.sleep(POLLING_INTERVAL)

    response = VideoStatus(**response)

    return response


class Videos:
    def __init__(self, auth):
        self.auth = auth

    def get(
        self,
        uid: str,
        expand: list = None
    ):
        endpoint = f"/video/{uid}"

        expand_parameter = None if expand is None else {"expand": ",".join(expand)}
        response = Request(self.auth).get(endpoint, params=expand_parameter)
        response = format_video_object(response)

        return response

    def delete(
        self,
        uid: str
    ):
        endpoint = f"/video/{uid}"
        response = Request(self.auth).delete(endpoint)
        response = VideoStatus(**response)

        return response
    
    def upload(
        self,
        path: str,
        collection: str
    ):
        response = _upload_video(path=path, auth=self.auth, collection=collection)

        return response

    def index(
        self,
        uid: str,
        wait: bool = False
    ):
        response = _index_video(uid=uid, auth=self.auth, wait=wait)

        return response
