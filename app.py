from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
CONVERTED_FOLDER = './converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

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

    # Save the uploaded image
    uploaded_image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(uploaded_image_path)

    # Open the image and convert it
    try:
        img = Image.open(uploaded_image_path)
        img = img.convert("RGB")  # Convert to RGB if it's not, to avoid issues with formats like PNG
        converted_filename = f"{os.path.splitext(file.filename)[0]}.{target_format.lower()}"
        converted_image_path = os.path.join(CONVERTED_FOLDER, converted_filename)
        img.save(converted_image_path, target_format)
    except Exception as e:
        return f"Error during conversion: {str(e)}", 500

    # Provide a download link
    download_link = f"/download/{converted_filename}"
    return render_template('index.html', download_link=download_link)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(CONVERTED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

