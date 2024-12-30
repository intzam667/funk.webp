from flask import Flask, request, render_template, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', download_link=None)

@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return 'No file part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    current_format = request.form['current_format']
    target_format = request.form['target_format']

    img = Image.open(file.stream)

    img = img.convert("RGB")

    img_io = io.BytesIO()
    img.save(img_io, target_format)
    img_io.seek(0)

    return send_file(img_io, mimetype=f'image/{target_format.lower()}', as_attachment=True, download_name=f'converted_image.{target_format.lower()}')

if __name__ == '__main__':
    app.run(debug=True)
