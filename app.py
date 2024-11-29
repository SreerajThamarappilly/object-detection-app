# app.py

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from utils.detector import ObjectDetector
from config import Config
import os

# Configuration class using OOP
class Config:
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = 'static/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
detector = ObjectDetector()  # Initialize the object detector

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload and redirect to results page."""
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Process the file
        if filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}:
            # Video processing
            output_path = detector.process_video(filepath)
        else:
            # Image processing with preprocessing
            output_path = detector.process_image(filepath)
        return redirect(url_for('results', filename=os.path.basename(output_path)))
    else:
        return redirect(url_for('index'))

@app.route('/results/<filename>')
def results(filename):
    """Display the results page with the processed image or video."""
    return render_template('results.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    """Serve the processed file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
