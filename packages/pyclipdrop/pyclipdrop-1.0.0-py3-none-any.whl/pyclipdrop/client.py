import os
import requests
from typing import Text, Dict

from pyclipdrop.settings import settings
from pyclipdrop.io_file_handlers import InputFileHandler, OutputFileHandler
from pyclipdrop.exceptions import APIRequestError, ValueTooLongError, ValueNotSupportedError, ValueOutOfRangeError


class ClipdropClient:
    """
    The client class for the Clipdrop API.

    Args:
        api_key (Text): The API key for the Clipdrop API.
        base_url (Text): The base URL for the Clipdrop API. The default value is maintained in the settings module.
        version (Text): The version of the Clipdrop API to use. The default value is maintained in the settings module.

    Raises:
        ValueError: If the API key is not passed to the client or set as an environment variable.
    """

    def __init__(self, api_key: Text = None, base_url: Text = settings.BASE_URL, version: Text = settings.VERSION) -> None:
        self.api_key = api_key or os.environ.get('CLIPDROP_API_KEY')
        if not self.api_key:
            raise ValueError("A Clipdrop API key must either be passed to the client or set as the CLIPDROP_API_KEY environment variable.")

        self.base_url = base_url
        self.version = version

    def text_to_image(self, prompt: Text, output_file: Text = 'output.png') -> None:
        """
        Generate an image from a text prompt.

        Args:
            prompt (Text): The text prompt to generate the image from.
            output_file (Text): The name of the output file. The default value is 'output.png'. The only supported extension is PNG.

        Raises:
            ValueError: If the path to the output file is not valid or the extension is not PNG.
            requests.exceptions.HTTPError: If the API request fails.        
        """
        # Check if prompt is less than 1000 characters
        if len(prompt) > 1000:
            raise ValueTooLongError("The prompt must be less than 1000 characters.")

        # Initialize the output handler
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.png'])

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/text-to-image/{self.version}',
            files={
                'prompt': (None, prompt, 'text/plain')
            }
        )

        output_file_handler.write(response.content)

    def replace_background(self, input_file: Text, prompt: Text = "", output_file: Text = None):
        """
        Replace the background of an image with a new background.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG, JPG (JPEG), and WEBP.
            prompt (Text): The text prompt to generate the new background from. The default value is an empty string.
            output_file (Text): The name of the output file. The default value is 'output' with the same extension as the input file. The extension of the output file must match the extension of the input file.

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension does not match that of the input file.
            requests.exceptions.HTTPError: If the API request fails.       
        """
        # Initialize the input handler
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg', '.webp'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # If the output file is not specified, use 'output' with the same extension as the input file
        if not output_file:
            output_file = f'output{input_extension}'

        # Initialize the output handler
        output_file_handler = OutputFileHandler(output_file, supported_extensions=[input_extension])

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/replace-background/{self.version}',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}')
            },
            data={
                'prompt': prompt
            }
        )

        output_file_handler.write(response.content)
        
    def remove_background(self, input_file: Text, transparency_handling: Text = None, output_file: Text = 'output.png'):
        """
        Remove the background of an image.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG, JPG (JPEG), and WEBP.
            transparency_handling (Text): The transparency handling mode for the output image. The default value is None. The supported values are 'return_input_if_non_opaque' and 'discard_alpha_layer',
            output_file (Text): The name of the output file. The default value is 'output.png'. The supported extensions are PNG, JPG (JPEG), and WEBP.

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not supported.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Check if transparency handling is supported
        if transparency_handling not in [None, 'return_input_if_non_opaque', 'discard_alpha_layer']:
            raise ValueNotSupportedError("The transparency handling mode must be either 'return_input_if_non_opaque' or 'discard_alpha_layer'.")

        # Initialize the input and output handlers
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg', '.webp'])
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.png', '.jpg', '.webp'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/remove-background/{self.version}',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}')
            },
            data={
                'transparency_handling': transparency_handling
            } if transparency_handling else {}
        )

        output_file_handler.write(response.content)

    def remove_text(self, input_file: Text, output_file: Text = 'output.png'):
        """
        Remove the text from an image.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG or JPG (JPEG).
            output_file (Text): The name of the output file. The default value is 'output.png'. The only supported extension is PNG.

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not PNG.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Initialize the input and output handlers
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg'])
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.png'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/remove-text/{self.version}',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}')
            }
        )

        output_file_handler.write(response.content)

    def reimagine(self, input_file: Text, output_file: Text = 'output.jpg'):
        """
        Reimagine an image.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG, JPG (JPEG), and WEBP.
            output_file (Text): The name of the output file. The default value is 'output.jpg'. The only supported extension is JPG (JPEG).

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not supported.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Initialize the input and output handlers
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg', '.webp'])
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.jpg'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()        

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/reimagine/{self.version}/reimagine',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}')
            }
        )

        output_file_handler.write(response.content)

    def sketch_to_image(self, input_file: Text, prompt: Text, output_file: Text = 'output.png'):
        """
        Generate an image from a sketch.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG, JPG (JPEG), and WEBP.
            prompt (Text): The text prompt describing the image to generate.
            output_file (Text): The name of the output file. The default value is 'output.jpg'. The only supported extension is JPG (JPEG).

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not PNG.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Check if prompt is less than 5000 characters
        if len(prompt) > 5000:
            raise ValueTooLongError("The prompt must be less than 5000 characters.")

        # Initialize the input and output handlers
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg', '.webp'])
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.jpg'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/sketch-to-image/{self.version}/sketch-to-image',
            files={
                'sketch_file': (input_file, image_data, f'image/{input_extension[1:]}'),
                'prompt': (None, prompt, 'text/plain')
            }
        )

        output_file_handler.write(response.content)

    def uncrop(self, input_file: Text, extend_up: int = 0, extend_down: int = 0, extend_left: int = 0, extend_right: int = 0, seed: int = None, output_file: Text = 'output.jpg'):
        """
        Generate new extensions of an image.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG, JPG (JPEG), and WEBP.
            extend_up (int): The number of pixels to extend the canvas up. The default value is 0.
            extend_down (int): The number of pixels to extend the canvas down. The default value is 0.
            extend_left (int): The number of pixels to extend the canvas left. The default value is 0.
            extend_right (int): The number of pixels to extend the canvas right. The default value is 0.
            seed (int): The seed for making the result deterministic. The default value is None.
            output_file (Text): The name of the output file. The default value is 'output.jpg'. The only supported extension is JPG (JPEG).

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not supported.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # TODO: Check if the extend values are within a valid range: negative values?

        # Initialize the input and output handlers
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg', '.webp'])
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.jpg'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # Check if the output file is valid
        output_file_handler.validate()

        # Add the data to the request
        data = {
            'extend_up': extend_up,
            'extend_down': extend_down,
            'extend_left': extend_left,
            'extend_right': extend_right
        }

        if seed:
            data['seed'] = seed

        response = self._submit_request(
            f'{self.base_url}/uncrop/{self.version}',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}')
            },
            data=data
        )

        output_file_handler.write(response.content)

    def image_upscaling(self, input_file: Text, target_width: int, target_height: int, output_file: Text = None):
        """
        Upscale an image to a target width and height.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG, JPG (JPEG), and WEBP.
            target_width (int): The target width of the output image in pixels.
            target_height (int): The target height of the output image in pixels.
            output_file (Text): The name of the output file. The default value is None, but if not specified, the output file will be 'output' with the relevant extension. The extension of the output file should be in the WEBP format if the image contains transparency, otherwise it should be in the JPG (JPEG).

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not supported.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Check if the target width and height are within the valid range of 1 and 4096
        if not 1 <= target_width <= 4096 or not 1 <= target_height <= 4096:
            raise ValueOutOfRangeError("The target width and height must be between 1 and 4096 pixels.")

        # Initialize the input handler
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg', '.webp'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        response = self._submit_request(
            f'{self.base_url}/image-upscaling/{self.version}/upscale',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}')
            },
            data={
                'target_width': target_width,
                'target_height': target_height
            }
        )

        # Get the output file extension from the response content type
        expected_output_extension = '.webp' if 'image/webp' in response.headers['Content-Type'] else '.jpg'

        # If the output file is not specified, use 'output' with the above extension
        if not output_file:
            output_file = f'output{expected_output_extension}'

        # Initialize the output handler
        output_file_handler = OutputFileHandler(output_file, supported_extensions=[expected_output_extension])

        # Check if the output file is valid
        output_file_handler.validate()

        output_file_handler.write(response.content)

    def cleanup(self, input_file: Text, mask_file: Text, mode: Text = 'fast', output_file: Text = 'output.png'):
        """
        Clean up an image using a mask.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG and JPG (JPEG).
            mask_file (Text): The name of the mask file. The only supported extension is PNG.
            mode (Text): The mode to use for cleaning up the image. The default value is 'fast'. The supported modes are 'fast' and 'quality'.
            output_file (Text): The name of the output file. The default value is 'output.png'. The only supported extension is PNG.

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the mask file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not PNG.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Check if the mode is supported
        if mode not in ['fast', 'quality']:
            raise ValueNotSupportedError("The mode must be either 'fast' or 'quality'.")

        # Initialize two input handlers for the input and mask files
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg'])
        mask_file_handler = InputFileHandler(mask_file, supported_extensions=['.png'])
        # Initialize the output handler
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.png'])

        # Check if the input files are valid
        input_file_handler.validate()
        mask_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # Get mask data and suffix
        mask_data = mask_file_handler.read()
        mask_suffix = mask_file_handler.get_extension()

        # Check if the output file is valid
        output_file_handler.validate()

        # Check if the mode is valid
        if mode not in ['fast', 'quality']:
            raise ValueError("The mode must be either 'fast' or 'quality'.")

        response = self._submit_request(
            f'{self.base_url}/cleanup/{self.version}',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}'),
                'mask_file': (mask_file, mask_data, f'image/{mask_suffix[1:]}')
            },
            data={
                'mode': mode
            }
        )

        output_file_handler.write(response.content)

    def portrait_depth_estimation(self, input_file: Text, output_file: Text = 'output.jpg'):
        """
        Estimate the depth of a portrait image.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG, JPG (JPEG), and WEBP.
            output_file (Text): The name of the output file. The default value is 'output.jpg'. The only supported extension is JPG (JPEG).

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not supported.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Initialize the input and output handlers
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg', '.webp'])
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.jpg'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/portrait-depth-estimation/{self.version}',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}')
            }
        )

        output_file_handler.write(response.content)

    def portrait_surface_normals(self, input_file: Text, output_file: Text = 'output.jpg'):
        """
        Generate surface normals of a portrait image.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG, JPG (JPEG), and WEBP.
            output_file (Text): The name of the output file. The default value is 'output.jpg'. The only supported extension is JPG (JPEG).

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not supported.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Initialize the input and output handlers
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg', '.webp'])
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.jpg'])

        # Check if the input file is valid
        input_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/portrait-surface-normals/{self.version}',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}')
            }
        )

        output_file_handler.write(response.content)

    def text_inpainting(self, input_file: Text, mask_file: Text, prompt: Text, output_file: Text = 'output.jpg'):
        """
        Inpaint text in an image.

        Args:
            input_file (Text): The name of the input file. The supported extensions are PNG and JPG (JPEG).
            mask_file (Text): The name of the mask file. The only supported extension is PNG.
            prompt (Text): The text prompt to generate the inpainted text.
            output_file (Text): The name of the output file. The default value is 'output.jpg'. The only supported extension is JPG (JPEG).

        Raises:
            ValueError: If the input file does not exist or the extension is not supported.
            ValueError: If the mask file does not exist or the extension is not supported.
            ValueError: If the path to the output file is not valid or the extension is not supported.
            requests.exceptions.HTTPError: If the API request fails.
        """
        # Initialize two input handlers for the input and mask files
        input_file_handler = InputFileHandler(input_file, supported_extensions=['.png', '.jpg'])
        mask_file_handler = InputFileHandler(mask_file, supported_extensions=['.png'])
        # Initialize the output handler
        output_file_handler = OutputFileHandler(output_file, supported_extensions=['.jpg'])

        # Check if the input files are valid
        input_file_handler.validate()
        mask_file_handler.validate()

        # Get input data and suffix
        image_data = input_file_handler.read()
        input_extension = input_file_handler.get_extension()

        # Get mask data and suffix
        mask_data = mask_file_handler.read()
        mask_suffix = mask_file_handler.get_extension()

        # Check if the output file is valid
        output_file_handler.validate()

        response = self._submit_request(
            f'{self.base_url}/text-inpainting/{self.version}',
            files={
                'image_file': (input_file, image_data, f'image/{input_extension[1:]}'),
                'mask_file': (mask_file, mask_data, f'image/{mask_suffix[1:]}'),
            },
            data={
                'text_prompt': prompt
            }
        )

        output_file_handler.write(response.content)

    def _submit_request(self, url: Text, files: Dict, data: Dict = None) -> requests.Response:
        """
        Submit a request to the Clipdrop API.

        Args:
            endpoint (Text): The endpoint of the API to submit the request to.
            files (Dict): A dictionary of files to submit with the request.
            data (Dict): A dictionary of data to submit with the request.

        Returns:
            requests.Response: The response object from the API request.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        response = requests.post(
            url,
            files=files,
            data=data,
            headers={
                'x-api-key': self.api_key
            }
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                error_message = response.json().get('error', 'No error message provided by the API')
            except ValueError:
                error_message = 'The response content from the API could not be decoded as JSON'
            raise APIRequestError(f"The request to the Clipdrop API failed: {error_message}") from e

        return response
