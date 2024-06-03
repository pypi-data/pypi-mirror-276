from typing import Text
from pathlib import Path
from urllib.parse import urlparse


def get_extension_from_file_path(file_path: Text) -> Text: 
    return Path(file_path).suffix


def get_extension_from_url(url: Text) -> Text:
    return Path(urlparse(url).path).suffix