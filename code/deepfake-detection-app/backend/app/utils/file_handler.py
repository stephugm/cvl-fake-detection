import os
from pathlib import Path
from werkzeug.utils import secure_filename

class FileHandler:
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = Path(upload_folder)
        self.allowed_extensions = allowed_extensions
        self.upload_folder.mkdir(exist_ok=True)
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def is_video(self, filename):
        """Check if file is a video"""
        return filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}
    
    def is_image(self, filename):
        """Check if file is an image"""
        return filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'bmp'}
    
    def save_file(self, file):
        """Save uploaded file and return path"""
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = self.upload_folder / filename
            file.save(str(filepath))
            return filepath
        return None
    
    def delete_file(self, filepath):
        """Delete file safely"""
        try:
            if filepath and Path(filepath).exists():
                os.remove(filepath)
                return True
        except Exception as e:
            print(f"Error deleting file: {e}")
        return False