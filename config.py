# config.py

import os
import secrets

class Config:
    """Configuration"""
    SECRET_KEY = secrets.token_hex(16)
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}
    MODEL_NAME = 'models/ssd_mobilenet_v2_coco_2018_03_29'
    PATH_TO_CKPT = os.path.join(MODEL_NAME, 'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join('utils', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90
