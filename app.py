from flask import Flask, redirect, url_for, render_template, request, session
import img2img
import txt2img

app = Flask(__name__)

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

@app.route("/text-to-image/encode/result", methods=['GET'])
def text2imageEncodeResult():
  return render_template('text-to-image-encode-result.html')

@app.route("/text-to-image/decode", methods=['GET', 'POST'])
def text2imageDecode():
  if request.method == 'GET':
    return render_template('text-to-image-decode.html')

@app.route("/text-to-image/decode/result", methods=['GET'])
def text2imageDecodeResult():
  return render_template('text-to-image-decode-result.html')

@app.route("/image-to-image", methods=['GET'])
def image2imageIndex():
  return render_template('image-to-image-index.html')

@app.route("/image-to-image/encode", methods=['GET', 'POST'])
def image2imageEncode():
  if request.method == 'GET':
    return render_template('image-to-image-encode.html')

@app.route("/image-to-image/encode/result", methods=['GET'])
def image2imageEncodeResult():
  return render_template('image-to-image-encode-result.html')

@app.route("/image-to-image/decode", methods=['GET', 'POST'])
def image2imageDecode():
  if request.method == 'GET':
    return render_template('image-to-image-decode.html')

@app.route("/image-to-image/decode/result", methods=['GET'])
def image2imageDecodeResult():
  return render_template('image-to-image-decode-result.html')


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)