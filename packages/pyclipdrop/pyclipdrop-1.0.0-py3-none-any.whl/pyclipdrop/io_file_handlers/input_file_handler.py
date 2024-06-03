import urllib.request
from pathlib import Path
from typing import Text, List
from urllib.parse import urlparse
from pyclipdrop.exceptions import FileOrURLError, FileOpenError, FileExtensionError, URLReadError
from pyclipdrop.utilities import get_extension_from_file_path, get_extension_from_url, is_extension_supported


class InputFileHandler:
    def __init__(self, input_file: Text, supported_extensions: List[Text] = None) -> None:
        self.input_file = input_file
        self.supported_extensions =  supported_extensions
        self.input_extension = None
        self.is_file = None

    def validate(self) -> None:
        if self._is_valid_file_path():
            self.set_is_file(True)
            self.set_extension(get_extension_from_file_path(self.input_file))

        elif self._is_valid_url():
            self.set_is_file(False)
            self.set_extension(get_extension_from_url(self.input_file))

        else:
            raise FileOrURLError("Input file must be a valid file path or URL.")

        if not is_extension_supported(self.get_extension(), self.supported_extensions):
            raise FileExtensionError(f"The input file should be one of the supported extensions: {" ".join(self.supported_extensions)}")
        
    def _is_valid_file_path(self) -> bool:
        return Path(self.input_file).exists()
    
    def _is_valid_url(self) -> bool:
        try:
            result = urlparse(self.input_file)
            return all([result.scheme, result.netloc])
        except AttributeError:
            return False
        
    def get_extension(self) -> Text:
        return self.input_extension
    
    def set_extension(self, extension: Text) -> None:
        self.input_extension = extension

    def get_is_file(self) -> bool:
        return self.is_file
    
    def set_is_file(self, is_file: bool) -> None:
        self.is_file = is_file
    
    def read(self) -> bytes:
        if self.get_is_file():
            return self._read_file(self.input_file)
        else:
            return self._read_url(self.input_file)
    
    def _read_file(self, file_path) -> bytes:
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except (PermissionError, OSError) as e:
            raise FileOpenError("Error opening file: " + str(e)) from e
        
    def _read_url(self, url) -> bytes:
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            raise URLReadError("Error in API request: " + str(e)) from e
