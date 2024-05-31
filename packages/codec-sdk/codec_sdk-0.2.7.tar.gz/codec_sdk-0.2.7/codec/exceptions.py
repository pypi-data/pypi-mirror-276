from codec.constants import (
    API_ERROR_CODES,
    COLLECTION_ERROR_CODES,
    INDEXING_ERROR_CODES,
    SEARCH_ERROR_CODES,
    UPLOAD_ERROR_CODES,
    VIDEO_ERROR_CODES
)

class APIException(Exception):
    pass

class CollectionException(Exception):
    pass

class IndexingException(Exception):
    pass

class SearchException(Exception):
    pass

class UploadException(Exception):
    pass

class VideoException(Exception):
    pass

class WebhookException(Exception):
    pass


def error_handler(error_code, error_message):
    if error_code in API_ERROR_CODES:
        raise APIException(error_message)
    
    elif error_code in COLLECTION_ERROR_CODES:
        raise CollectionException(error_message)

    elif error_code in INDEXING_ERROR_CODES:
        raise IndexingException(error_message)

    elif error_code in SEARCH_ERROR_CODES:
        raise SearchException(error_message)
    
    elif error_code in UPLOAD_ERROR_CODES:
        raise UploadException(error_message)
    
    elif error_code in VIDEO_ERROR_CODES:
        raise VideoException(error_message)
    
    else:
        raise APIException("An unknown error occured.")
