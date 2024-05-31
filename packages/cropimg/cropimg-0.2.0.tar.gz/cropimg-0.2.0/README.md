# Image Cropper Web Application

## Overview

This is a web application for cropping images interactively using a canvas interface. The application allows users to:

- Select an image from a dropdown list.
- Draw a rectangle on the canvas to specify the crop area.
- Save the cropped image with a specified file name.
- Update and fetch images dynamically from a server.

## Features

- Interactive image cropping using a canvas interface.
- Real-time preview of the cropped area.
- Dynamic image list fetching and updating.
- Error handling and notifications.

## Installation

### Clone the Repository

To install and set up this project, follow the steps below:

1. Clone the repository:
    ```bash
    git clone https://github.com/ShotaIuchi/crop-image.git
    cd cropimg
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    cd cropimg
    python cropimg.py
    ```

### Install via `pip`

If the package is available on PyPI, you can install it using `pip`:

1. Install the package:
    ```bash
    pip install cropimg
    ```

2. Run the application:
    ```bash
    cropimg
    ```

## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Use the dropdown list to select an image.
3. Draw a rectangle on the canvas to specify the crop area.
4. Enter the desired file name in the form and click "Crop Image" to save the cropped image.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or inquiries, please contact [shotaiuchi.develop@gmail.com](mailto:shotaiuchi.develop@gmail.com)

