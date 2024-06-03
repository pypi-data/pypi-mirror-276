from pathlib import Path
from typing import Text, List
from pyclipdrop.utilities import get_extension_from_file_path, is_extension_supported
from pyclipdrop.exceptions import FilePathError, FileExtensionError, FileOpenError, FileWriteError


class OutputFileHandler:
    def __init__(self, output_file: Text, supported_extensions: List[Text] = None) -> None:
        self.output_file = output_file
        self.supported_extensions = supported_extensions
        self.output_extension = None

    def validate(self) -> None:
        if self._is_valid_parent_directory():
            self.set_extension(get_extension_from_file_path(self.output_file))

        else:
            raise FilePathError("The path to the output file does not exist.")
        
        if not is_extension_supported(self.output_extension, self.supported_extensions):
            raise FileExtensionError(f"The output file should be one of the supported extensions: {" ".join(self.supported_extensions)}")
        
    def _is_valid_parent_directory(self) -> bool:
        return Path(self.output_file).parent.exists()
    
    def set_extension(self, extension: Text) -> Text:
        self.output_extension = extension
        
    def write(self, data: bytes) -> None:
        try:
            with open(self.output_file, 'wb') as f:
                try:
                    f.write(data)
                except (IOError, OSError) as e:
                    raise FileWriteError("Error writing to file: " + str(e))
        except (FileNotFoundError, PermissionError, OSError) as e:
            raise FileOpenError("Error opening file: " + str(e))
