import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    UPLOAD_FOLDER = BASE_DIR / os.getenv('UPLOAD_FOLDER', 'uploads')
    MODEL_PATH = BASE_DIR / os.getenv('MODEL_PATH', 'app/models/efficientnet-ariq.pth')
    
    # Face Detection
    FACE_DETECTION_CONFIDENCE = float(os.getenv('FACE_DETECTION_CONFIDENCE', 0.9))
    IMG_SIZE = (int(os.getenv('IMG_SIZE', 224)), int(os.getenv('IMG_SIZE', 224)))
    
    # Video Processing
    FRAMES_PER_VIDEO = int(os.getenv('FRAMES_PER_VIDEO', 30))
    FRAME_SKIP = int(os.getenv('FRAME_SKIP', 3))
    
    # File Upload
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,mp4,avi,mov').split(','))
    
    # Ensure upload folder exists
    UPLOAD_FOLDER.mkdir(exist_ok=True)