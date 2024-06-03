from typing import Text
from pydantic_settings import BaseSettings


class PyClipdropSettings(BaseSettings):
    """
    Settings for the PyClipdrop package.

    Attributes:
        BASE_URL (Text): Base URL for the Clipdrop API.
        VERSION (Text): Version of the Clipdrop API.
    """

    BASE_URL: Text = "https://clipdrop-api.co"
    VERSION: Text = "v1"


settings = PyClipdropSettings()