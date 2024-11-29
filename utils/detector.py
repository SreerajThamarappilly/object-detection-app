# utils/detector.py

import tensorflow as tf
import numpy as np
import cv2
import os
from utils import label_map_util
from utils import visualization_utils as vis_util
from PIL import Image

class ObjectDetector:
    """Object Detector class using SSD MobileNet V2."""

    def __init__(self):
        """Initialize the model and load label maps."""
        self.model_name = 'models/ssd_mobilenet_v2_coco_2018_03_29'
        self.path_to_ckpt = os.path.join(self.model_name, 'frozen_inference_graph.pb')
        self.path_to_labels = 'utils/mscoco_label_map.pbtxt'
        self.num_classes = 90
        self.load_model()
        self.load_label_map()

    def load_model(self):
        """Load the TensorFlow model into memory."""
        self.detection_model = tf.saved_model.load(self.model_name + '/saved_model')

    def load_label_map(self):
        """Load label maps."""
        self.category_index = label_map_util.create_category_index_from_labelmap(
            self.path_to_labels, use_display_name=True)

    def preprocess_image(self, image):
        """Preprocess the image for detection."""
        # Resize image
        image_resized = image.resize((300, 300))
        # Normalize image
        image_np = np.array(image_resized) / 255.0
        image_np_expanded = np.expand_dims(image_np, axis=0)
        return image_np_expanded

    def process_image(self, image_path):
        """Perform object detection on an image."""
        image = Image.open(image_path)
        image_np = np.array(image)
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        # Run detection
        detections = self.detection_model(input_tensor)
        # Visualization
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            detections['detection_boxes'][0].numpy(),
            detections['detection_classes'][0].numpy().astype(np.int32),
            detections['detection_scores'][0].numpy(),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8)
        # Save the image
        output_path = image_path.rsplit('.', 1)[0] + '_output.jpg'
        output_image = Image.fromarray(image_np)
        output_image.save(output_path)
        return output_path

    def process_video(self, video_path):
        """Perform object detection on a video."""
        cap = cv2.VideoCapture(video_path)
        output_path = video_path.rsplit('.', 1)[0] + '_output.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Convert frame to tensor
            input_tensor = tf.convert_to_tensor(frame)
            input_tensor = input_tensor[tf.newaxis, ...]
            # Run detection
            detections = self.detection_model(input_tensor)
            # Visualization
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                detections['detection_boxes'][0].numpy(),
                detections['detection_classes'][0].numpy().astype(np.int32),
                detections['detection_scores'][0].numpy(),
                self.category_index,
                use_normalized_coordinates=True,
                line_thickness=8)
            # Write the frame
            if out is None:
                height, width, _ = frame.shape
                out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))
            out.write(frame)
        cap.release()
        out.release()
        return output_path
