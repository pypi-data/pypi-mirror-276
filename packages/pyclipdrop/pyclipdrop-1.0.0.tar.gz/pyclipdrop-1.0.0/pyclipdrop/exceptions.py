
class APIRequestError(Exception):
    """
    Exception raised for errors in the API request to Clipdrop.
    """
    pass


class FileOrURLError(Exception):
    """
    Exception raised for invalid file paths or URLs.
    """
    pass


class FilePathError(Exception):
    """
    Exception raised for when a file path does not exist.
    """
    pass


class FileOpenError(Exception):
    """
    Exception raised for errors in opening a file.
    """
    pass


class FileWriteError(Exception):
    """
    Exception raised for errors in writing to a file.
    """
    pass


class FileExtensionError(Exception):
    """
    Exception raised when a file extension is not supported.
    """
    pass


class URLReadError(Exception):
    """
    Exception raised for errors in reading from a URL.
    """
    pass


class ValueOutOfRangeError(Exception):
    """
    Exception raised when an input is out of an expected range.
    """
    pass


class ValueTooLongError(Exception):
    """
    Exception raised when an input is too long.
    """
    pass


class ValueNotSupportedError(Exception):
    """
    Exception raised when an input is not supported.
    """
    pass