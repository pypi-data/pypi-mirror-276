from typing import Text, List


def is_extension_supported(extension: Text, supported_extensions: List) -> bool:
    supported_extensions = supported_extensions + ['.jpeg'] if '.jpg' in supported_extensions else supported_extensions
    return extension in supported_extensions