from codec import __version__


API_VERSION = "v1"
BASE_ENDPOINT = "https://api.codec.io"
BASE_URL = f"{BASE_ENDPOINT}/{API_VERSION}"
CLIENT = f"python/{__version__}"
SUPABASE_URL = "https://db.codec.io"
SUPABASE_PUBLIC_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN2anZpdGF4Y29wbGlsbml5a211Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDcyMTk0MDAsImV4cCI6MjAyMjc5NTQwMH0.CtGEgKX-WYNSsclRMnW_nl2ydpKzBjv_ybVmeGMUc8Y"

SUPPORTED_VIDEO_FORMATS = [
    "mp4"
]

REQUEST_TIMEOUT = 10
POLLING_INTERVAL = 5
TIMEOUT_MESSAGE = "Your request cannot be processed at this time due to a timeout from the upstream server. Please try again later. If the issue persists, check our status page https://status.codec.io or contact support@codec.io for assistance."
API_ERROR_CODES = [
    "unknown_error",
    "gateway_timeout",
    "too_many_requests",
    "auth.not_found",
    "auth.not_team_owner",
    "expand.invalid_keys",
    "auth.payment_required"
]
COLLECTION_ERROR_CODES = [
    "collections.invalid_name",
    "collections.not_found"
]
INDEXING_ERROR_CODES = [
    "indexer.video_not_found"
]
SEARCH_ERROR_CODES = [
    "search.invalid_max_results",
    "search.invalid_types"
]
UPLOAD_ERROR_CODES = [
    "uploads.invalid_filename"
]
VIDEO_ERROR_CODES = [
    "videos.not_found"
]
