 Image Input Handler

`image-input-handler` is a versatile Python package designed to simplify the handling of various image inputs. It supports images from multiple sources including file paths, URLs, and base64 encoded strings. It adjusts image channels according to user needs and includes functionality for checking compatibility and enabling debug mode, making it an essential tool for projects involving image processing.

## Features

- Handle images from URLs, file paths, and base64 strings.
- Automatic adjustment of image channels.
- Support for image masks.
- Compatibility checks to ensure image inputs can be processed.
- Debug mode for detailed operational logging, aiding in troubleshooting and development.
- Easy integration with popular libraries such as NumPy, OpenCV, and PIL.

## Installation

Install `image-input-handler` using pip:

```bash``` pip install image-input-handler

# Usage
Below is a basic example of how to use image-input-handler:
```
from image_input_handler import UniversalImageInputHandler

# Initialize the handler with a local file path, enabling debug mode
handler = UniversalImageInputHandler('path/to/your/image.png', debug=True)

# For URL based images
url_handler = UniversalImageInputHandler('http://example.com/image.png')

# For base64 encoded images
base64_handler = UniversalImageInputHandler('base64_encoded_string_here', img_is_a_mask=True)

# Access the processed image
processed_image = handler.img

# Check if the image is compatible
if handler.COMPATIBLE:
    print("The image is compatible.")
else:
    print("The image is not compatible.")



