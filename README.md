# object-detection-app

An object detection web application that processes images and videos to detect objects using a pre-trained machine learning model. The application is built with TensorFlow, OpenCV and Flask, and implements object-oriented principles and design patterns for maintainability and scalability.

## Features

- Upload images or videos for object detection.
- Supports image preprocessing for better accuracy.
- Processes videos frame by frame.
- Responsive user interface compatible with all devices.

## Technologies and Concepts Used

- **Python 3.11**
- **TensorFlow**: Deep learning framework for object detection.
- **OpenCV**: Image processing and video handling.
- **Flask**: Web framework for building the application.

## Directory Structure

```bash
object-detection-app/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings and environment variables
├── static/
│   ├── css/
│   │   └── styles.css          # Custom styles for the application
│   └── uploads/                # Folder for storing uploaded files
├── templates/
│   ├── base.html               # Base template for consistent layout
│   ├── index.html              # Upload page
│   └── results.html            # Results display page
├── utils/
│   ├── detector.py             # ObjectDetector class for model handling
│   ├── label_map_util.py       # Utility for label map parsing
│   ├── visualization_utils.py  # Visualization tools for detected objects
│   ├── mscoco_label_map.pbtxt
├── models/
│   └── ssd_mobilenet_v2_coco_2018_03_29
├── requirements.txt            # Dependencies for the project
├── README.md
```

- **Object-Oriented Principles**:
    - **Encapsulation**: Logical grouping of related functions in classes (e.g., ObjectDetector).
    - **Abstraction**: Hiding implementation details through public methods.
  - - **Inheritance**: Base components are reusable for extending features.

- **Design Patterns**:
    - **Singleton Pattern**: Ensures a single instance of shared resources (e.g., model loader).
    - **Factory Pattern**: Creates objects dynamically for extensibility (e.g., loading models).

- **Advanced Concepts**:
    - **Responsive Design**: Ensures the application adapts seamlessly to various devices.
    - **Environment Variables**: Securely manage sensitive data such as secret keys.

## Environment Variables

```bash
SECRET_KEY=your_generated_secret_key
UPLOAD_FOLDER=static/uploads/
ALLOWED_EXTENSIONS=png,jpg,jpeg,mp4,avi,mov
```

## Running the Application Locally

```bash
pip install -r requirements.txt
python app.py
```

## Testing the Application

```bash
/                           GET         Home page with upload form.
/upload                     POST        Process uploaded file.
/results                    GET         Display detection results.
/uploads/<filename>         GET         Serve uploaded files.
```

## License

*This project is licensed under the MIT License.*
