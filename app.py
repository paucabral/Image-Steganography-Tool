from flask import Flask, flash, redirect, url_for, render_template, request, session
from werkzeug.utils import secure_filename
from settings import *
import os
from datetime import datetime
import img2img
import txt2img

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

UPLOAD_FOLDER = UPLOAD_DIR
if not os.path.exists('./{}'.format(UPLOAD_FOLDER)):
    os.makedirs('./{}'.format(UPLOAD_FOLDER))
ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/text-to-image", methods=['GET'])
def text2imageIndex():
    return render_template('text-to-image-index.html')


@app.route("/text-to-image/encode", methods=['GET', 'POST'])
def text2imageEncode():
    if request.method == 'GET':
        return render_template('text-to-image-encode.html')

    elif request.method == 'POST':
        # check if the post request has the file part
        if 'cover_img' not in request.files:
            print('No file part')
            return redirect(request.url)
        cover_image = request.files['cover_img']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if cover_image.filename == '':
            print('No selected file')
            return redirect(request.url)
        if cover_image and allowed_file(cover_image.filename):
            cover_image_filename = secure_filename(
                datetime.now().strftime("%m-%d-%Y-%H-%M-%S-") + cover_image.filename)
            cover_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'], cover_image_filename))
            cover_image_filepath = os.path.join(
                app.config['UPLOAD_FOLDER'], cover_image_filename)
        if request.form.get('password'):
            password = request.form.get('password')
        else:
            password = None
        message = request.form.get('message')
        steg_image_filepath = '{}-steg.png'.format(cover_image_filepath)

        # EXECUTE ENCODING
        msg = txt2img.encode(input_filepath=cover_image_filepath, text=message,
                             output_filepath=steg_image_filepath, password=password)

        if type(msg) == str:
            if 'Error:' in msg:
                flash(msg)
                return render_template('text-to-image-encode.html')

        session["steg_image"] = steg_image_filepath
        return redirect('/text-to-image/encode/result')


@app.route("/text-to-image/encode/result", methods=['GET'])
def text2imageEncodeResult():
    if 'steg_image' in session:
        steg_image = session['steg_image']
        return render_template('text-to-image-encode-result.html', steg_image=steg_image)
    else:
        return redirect('/')


@app.route("/text-to-image/decode", methods=['GET', 'POST'])
def text2imageDecode():
    if request.method == 'GET':
        return render_template('text-to-image-decode.html')
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'steg_img' not in request.files:
            print('No file part')
            return redirect(request.url)
        steg_image = request.files['steg_img']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if steg_image.filename == '':
            print('No selected file')
            return redirect(request.url)
        if steg_image and allowed_file(steg_image.filename):
            steg_image_filename = secure_filename(steg_image.filename)
            steg_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'], steg_image_filename))
            steg_image_filepath = os.path.join(
                app.config['UPLOAD_FOLDER'], steg_image_filename)
        if request.form.get('password'):
            password = request.form.get('password')
        else:
            password = None

        # EXECUTE ENCODING
        message = txt2img.decode(
            input_filepath=steg_image_filepath, password=password)

        if 'Error:' in message:
            flash(message)
            return render_template('text-to-image-decode.html')

        session["steg_message"] = message
        return redirect('/text-to-image/decode/result')


@app.route("/text-to-image/decode/result", methods=['GET'])
def text2imageDecodeResult():
    if 'steg_message' in session:
        steg_message = session['steg_message']
        return render_template('text-to-image-decode-result.html', steg_message=steg_message)
    else:
        return redirect('/')


@app.route("/image-to-image", methods=['GET'])
def image2imageIndex():
    return render_template('image-to-image-index.html')


@app.route("/image-to-image/encode", methods=['GET', 'POST'])
def image2imageEncode():
    if request.method == 'GET':
        return render_template('image-to-image-encode.html')
    elif request.method == 'POST':
        # COvER IMG
        # check if the post request has the file part
        if 'cover_img' not in request.files:
            print('No file part')
            return redirect(request.url)
        cover_image = request.files['cover_img']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if cover_image.filename == '':
            print('No selected file')
            return redirect(request.url)
        if cover_image and allowed_file(cover_image.filename):
            cover_image_filename = secure_filename(
                datetime.now().strftime("%m-%d-%Y-%H-%M-%S-") + cover_image.filename)
            cover_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'], cover_image_filename))
            cover_image_filepath = os.path.join(
                app.config['UPLOAD_FOLDER'], cover_image_filename)

        # SECRET IMG
        # check if the post request has the file part
        if 'secret_img' not in request.files:
            print('No file part')
            return redirect(request.url)
        secret_image = request.files['secret_img']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if secret_image.filename == '':
            print('No selected file')
            return redirect(request.url)
        if secret_image and allowed_file(secret_image.filename):
            secret_image_filename = secure_filename(
                datetime.now().strftime("%m-%d-%Y-%H-%M-%S-") + secret_image.filename)
            secret_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'], secret_image_filename))
            secret_image_filepath = os.path.join(
                app.config['UPLOAD_FOLDER'], secret_image_filename)

        steg_image_filepath = '{}-{}-steg.png'.format(
            cover_image_filepath, secret_image_filename)

        # EXECUTE ENCODING
        msg = img2img.merge(COVER_IMG_FILEPATH=cover_image_filepath,
                            SECRET_IMG_FILEPATH=secret_image_filepath, OUTPUT_IMG_FILEPATH=steg_image_filepath)

        if type(msg) == str:
            if 'Error:' in msg:
                flash(msg)
                return render_template('image-to-image-encode.html')

        session["steg_image"] = steg_image_filepath
        return redirect('/image-to-image/encode/result')


@app.route("/image-to-image/encode/result", methods=['GET'])
def image2imageEncodeResult():
    if 'steg_image' in session:
        steg_image = session['steg_image']
        return render_template('image-to-image-encode-result.html', steg_image=steg_image)
    else:
        return redirect('/')


@app.route("/image-to-image/decode", methods=['GET', 'POST'])
def image2imageDecode():
    if request.method == 'GET':
        return render_template('image-to-image-decode.html')
    elif request.method == 'POST':
        # STEG IMG
        # check if the post request has the file part
        if 'steg_img' not in request.files:
            print('No file part')
            return redirect(request.url)
        steg_image = request.files['steg_img']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if steg_image.filename == '':
            print('No selected file')
            return redirect(request.url)
        if steg_image and allowed_file(steg_image.filename):
            steg_image_filename = secure_filename(
                datetime.now().strftime("%m-%d-%Y-%H-%M-%S-") + steg_image.filename)
            steg_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'], steg_image_filename))
            steg_image_filepath = os.path.join(
                app.config['UPLOAD_FOLDER'], steg_image_filename)

        decoded_image_filepath = '{}-decoded.png'.format(steg_image_filepath)

        # EXECUTE ENCODING
        msg = img2img.unmerge(ENCODED_IMG_FILEPATH=steg_image_filepath,
                              OUTPUT_IMG_FILEPATH=decoded_image_filepath)

        if type(msg) == str:
            if 'Error:' in msg:
                flash(msg)
                return render_template('image-to-image-encode.html')

        session["decoded_image"] = decoded_image_filepath
        return redirect('/image-to-image/decode/result')


@app.route("/image-to-image/decode/result", methods=['GET'])
def image2imageDecodeResult():
    if 'decoded_image' in session:
        decoded_image = session['decoded_image']
        return render_template('image-to-image-decode-result.html', decoded_image=decoded_image)
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
