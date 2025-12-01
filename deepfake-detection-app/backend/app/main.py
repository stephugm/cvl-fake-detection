from flask import Flask
from flask_cors import CORS
from tensorflow.keras.models import load_model
import torch
from torchvision import models
import os

from app.config import Config
from app.routes.detection import detection_bp, init_detection_routes
from app.services.face_detector import FaceDetector
from app.services.image_processor import ImageProcessor
from app.services.video_processor import VideoProcessor
from app.utils.file_handler import FileHandler

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Load ML model
    model = None
    print(f"Loading model from: {Config.MODEL_PATH}")
    try:
        is_pytorch = Config.MODEL_PATH.suffix.lower() == '.pth'
        if is_pytorch:
            model = torch.load(str(Config.MODEL_PATH), weights_only=False, map_location=torch.device('cpu'))
            print(f"✅ Model loaded successfully")
        else:
            model = load_model(str(Config.MODEL_PATH))
            print(f"✅ Model loaded successfully")
            print(f"   Input shape: {model.input_shape}")
            print(f"   Output shape: {model.output_shape}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print(f"⚠️ Running without model (will return dummy predictions)")
        model = None
    
    # Initialize services
    face_detector = FaceDetector(
        confidence_threshold=Config.FACE_DETECTION_CONFIDENCE
    )
    
    file_handler = FileHandler(
        upload_folder=Config.UPLOAD_FOLDER,
        allowed_extensions=Config.ALLOWED_EXTENSIONS
    )
    
    image_processor = ImageProcessor(
        face_detector=face_detector,
        model=model
    )
    
    video_processor = VideoProcessor(
        face_detector=face_detector,
        model=model,
        frame_skip=Config.FRAME_SKIP
    )
    
    # Initialize routes with dependencies
    init_detection_routes(file_handler, image_processor, video_processor)
    
    # Register blueprints
    app.register_blueprint(detection_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)