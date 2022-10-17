# Importing
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
import os
import sys


# Importing custom libs
sys.path.insert(0, 'libraries')
from steganography import encode_to_img, decode_from_img, get_img_capacity
from helpers import remove_all_from_dir, validate_input_encode, validate_input_decode


# Env setup
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "images"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# Flask endpoints
@app.route('/', methods=["GET"])
def main_page():
    if request.method == 'GET':
        return render_template("choice.html")


@app.route('/encode', methods=["GET", "POST"])
def encode():
    if request.method == 'GET':
        return render_template("encode.html", error_data = {})

    # First validate input data
    validity, error_data = validate_input_encode(request.form, request.files)
    if not validity:
        return render_template("encode.html", error_data = error_data, was_validated = "was-validated")

    # At this point we are sure the data is valid
    image = request.files["image"]
    message = request.form["message"]

    # Remove old image/s
    remove_all_from_dir("images")
    remove_all_from_dir("encoded_images")

    # Save new image
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
    image.save(img_path)

    # Generate encoded image
    encoded_img_name = secure_filename(image.filename).split('.')[0] + "_encoded.png"
    encoded_img_path = f"encoded_images/{encoded_img_name}"
    try:
        result = encode_to_img(img_path, message, encoded_img_path)
        if "ERROR" in result:
            return render_template("error.html", error_message = result)
    except:
        return render_template("error.html", error_message = "Oops, this wasn't supposed to happen. Try again.")
    
    
    img_capacity = get_img_capacity(img_path)
    if "ERROR" in img_capacity:
        return render_template("error.html", error_message = img_capacity)

    return render_template("encode_success.html", img_capacity = img_capacity, download_path = encoded_img_path)


@app.route('/decode', methods=["GET", "POST"])
def decode():
    if request.method == 'GET':
        return render_template("decode.html", error_data = {})

    # First validate input data
    validity, error_data = validate_input_decode(request.files)
    if not validity:
        return render_template("decode.html", error_data = error_data, was_validated = "was-validated")

    # At this point we are sure the data is valid
    image = request.files["image"]
    
    # Remove old image/s
    remove_all_from_dir("images_to_decode")

    # Decode message from encoded image
    img_path = os.path.join("images_to_decode", secure_filename(image.filename))
    image.save(img_path)
    try:
        message = decode_from_img(img_path)
    except:
        return render_template("error.html", error_message = "Oops, this wasn't supposed to happen. Try again.")

    return render_template("decode.html", decoded_message = message, error_data = {})


@app.route('/download', methods=["GET"])
def download():
    if request.method == 'GET':
        encoded_img_path = request.args.get("path")

        if encoded_img_path.strip() == "":
            return render_template("error.html", error_message = "Oh no, the path to the image looked very empty. Try again.")

        try:
            return send_file(encoded_img_path, as_attachment=True)
        except:
            return render_template("error.html", error_message = "Gosh, looks like the file you are looking for is not here.")


if __name__ == "__main__":
    app.run()