from flask import Flask, render_template, request, send_file
from moviepy.editor import VideoFileClip
import os
import uuid
import tempfile
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Temporary storage path (Vercel serverless functions only allow temporary storage)
UPLOAD_FOLDER = '/tmp/uploads/'
CONVERTED_FOLDER = '/tmp/converted_files/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Allowed formats
VIDEO_FORMATS = ['MP4', 'AVI', 'WEBM']

@app.route('/')
def index():
    return render_template('index.html', download_link=None)

@app.route('/convert', methods=['POST'])
def convert():
    current_video_format = request.form.get('current_video_format')
    target_video_format = request.form.get('target_video_format')
    
    video_file = request.files.get('video')

    # Handle video conversion
    if video_file:
        filename = secure_filename(video_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        video_file.save(file_path)

        # Generate unique file name for the converted video
        output_filename = str(uuid.uuid4()) + '.' + target_video_format.lower()
        output_file_path = os.path.join(CONVERTED_FOLDER, output_filename)

        # Convert video using moviepy
        try:
            video_clip = VideoFileClip(file_path)

            # Choose appropriate conversion method based on target format
            if target_video_format == 'MP4':
                video_clip.write_videofile(output_file_path, codec='libx264')
            elif target_video_format == 'AVI':
                video_clip.write_videofile(output_file_path, codec='libxvid')
            elif target_video_format == 'WEBM':
                video_clip.write_videofile(output_file_path, codec='libvpx')

            video_clip.close()

            download_link = os.path.join(CONVERTED_FOLDER, output_filename)

        except Exception as e:
            download_link = None
            print(f"Error during video conversion: {e}")

    return render_template('index.html', download_link=download_link)

if __name__ == "__main__":
    app.run(debug=True)
