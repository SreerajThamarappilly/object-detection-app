# app.py

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from utils.detector import ObjectDetector
from config import Config
import os
from time import time

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
        return render_template('error.html', message="No file uploaded"), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            # Process the file (image or video)
            if filename.lower().endswith(('mp4', 'avi', 'mov')):
                output_path = detector.process_video(filepath)
            else:
                output_path = detector.process_image(filepath)

            return redirect(url_for('results', filename=os.path.basename(output_path)))
        except Exception as e:
            return render_template('error.html', message=f"Processing error: {str(e)}"), 500
    else:
        return render_template('error.html', message="Invalid file type"), 400

@app.route('/results/<filename>')
def results(filename):
    """Display the results page with the processed image or video."""
    cache_bust = int(time())  # Generate a timestamp
    return render_template('results.html', filename=filename, cache_bust=cache_bust)

@app.route('/uploads/<filename>')
def send_file(filename):
    """Serve the processed file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.context_processor
def inject_time():
    """Inject the `time` module into all templates."""
    return {'time': time}

if __name__ == '__main__':
    app.run(debug=True)
