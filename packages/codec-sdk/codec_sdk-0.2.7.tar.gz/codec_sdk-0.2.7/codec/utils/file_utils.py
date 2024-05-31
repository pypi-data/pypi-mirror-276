from codec.constants import SUPPORTED_VIDEO_FORMATS
from codec.exceptions import VideoException
from pathlib import Path


def validate_path_and_get_filename(path):
    file_path = Path(path)
    file_exists = file_path.exists()
    if not file_exists:
        raise VideoException(f"File \"{path}\" does not exist")

    file_format_is_supported = bool(file_path.suffix.lower() in [f".{ff}" for ff in SUPPORTED_VIDEO_FORMATS])
    if not file_format_is_supported:
        raise VideoException(f"Invalid format for {path}. Supported formats: {', '.join(SUPPORTED_VIDEO_FORMATS)}")

    filename = file_path.name

    return filename
