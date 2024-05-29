#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import io
import os
import base64
from flask import Flask, request, send_file, render_template, abort, jsonify
from PIL import Image
from cropimg.update_image import UpdateImage
from cropimg.update_image_adb import *

# Input image file path
IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'static', 'input.png')

# Output image directory
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')

# Flask engine
app = Flask(__name__, template_folder='.')

# Update image object name
g_update_image_name: str = UpdateImage.s_update_func_list[0].get_name()


@app.route('/')
def home():
    return render_template('index.html', image_file=IMAGE_PATH)


@app.route('/crop', methods=['POST'])
def crop():
    # request parameters
    startX = request.form.get('startX', type=int, default=0)
    startY = request.form.get('startY', type=int, default=0)
    endX = request.form.get('endX', type=int, default=0)
    endY = request.form.get('endY', type=int, default=0)
    filename = request.form.get('filename', default=f'{datetime.now().strftime("%Y%m%dT%H%M%S")}.png')

    # Input validation
    if not filename.strip():
        return "File name is required.", 400

    # Normalize coordinates
    if startX > endX:
        startX, endX = endX, startX
    if startY > endY:
        startY, endY = endY, startY

    if startX == endX or startY == endY:
        return "Invalid rectangle coordinates.", 400

    # ensure filename has .png extension
    if not filename.lower().endswith('.png'):
        filename += '.png'

    # load image
    img_path = os.path.join(app.root_path, 'static', IMAGE_PATH)
    if not os.path.exists(img_path):
        abort(404, description="Image not found")

    # open image
    img = Image.open(img_path)

    # crop image
    cropped_img = img.crop((startX, startY, endX, endY))

    # save image to output directory
    os.makedirs(os.path.join(app.root_path, OUTPUT_DIR), exist_ok=True)
    cropped_img.save(os.path.join(app.root_path, OUTPUT_DIR, filename))

    # response image to client
    img_io = io.BytesIO()
    cropped_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@app.route('/image_list', methods=['GET'])
def image_list():
    images: list = []
    for ui in UpdateImage.s_update_func_list:
        images.append(ui.get_name())
    return jsonify({"images": images})


@app.route('/get_image', methods=['GET'])
def get_image():
    if os.path.exists(IMAGE_PATH):
        with open(IMAGE_PATH, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return jsonify({"image": encoded_image})
    else:
        return jsonify({"error": "Image not found"}), 404


@app.route('/update_image', methods=['POST'])
def update_image():
    global g_update_image_name
    data = request.json
    image_src = data.get('image', g_update_image_name)
    update_image: UpdateImage = None
    for ui in UpdateImage.s_update_func_list:
        if ui.get_name() == image_src:
            update_image = ui
            break
    try:
        update_image.update(IMAGE_PATH)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
