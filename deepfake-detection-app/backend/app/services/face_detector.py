import cv2
import numpy as np
from mtcnn import MTCNN

class FaceDetector:
    def __init__(self, confidence_threshold=0.7):
        """Initialize MTCNN face detector"""
        self.detector = MTCNN()
        self.confidence_threshold = confidence_threshold
    
    def extract_face_from_frame(self, frame, margin=5):
        """
        Extract face region from a frame using MTCNN
        
        Args:
            frame: Input frame (RGB format)
            margin: Pixel margin around detected face
        
        Returns:
            Extracted face region or None if no face detected
        """
        # Detect faces
        detections = self.detector.detect_faces(frame)
        
        if len(detections) == 0:
            return None
        
        # Get the face with highest confidence
        best_detection = max(detections, key=lambda x: x['confidence'])
        
        # Check confidence threshold
        if best_detection['confidence'] < self.confidence_threshold:
            return None
        
        # Extract bounding box
        x, y, w, h = best_detection['box']
        
        # Add margin
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(frame.shape[1], x + w + margin)
        y2 = min(frame.shape[0], y + h + margin)
        
        # Extract face region
        face = frame[y1:y2, x1:x2]
        
        return face
    
    def preprocess_face(self, face, target_size=(224, 224)):
        """
        Preprocess face for model input
        
        Args:
            face: Face region (RGB format)
            target_size: Target size for resizing
        
        Returns:
            Preprocessed face ready for model input
        """
        if face is None or face.size == 0:
            return None
        
        # Resize to target size
        face_resized = cv2.resize(face, target_size)
        
        return face_resized