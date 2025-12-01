from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

detection_bp = Blueprint('detection', __name__)

# These will be injected by main.py
file_handler = None
image_processor = None
video_processor = None

def init_detection_routes(fh, ip, vp):
    """Initialize route dependencies"""
    global file_handler, image_processor, video_processor
    file_handler = fh
    image_processor = ip
    video_processor = vp

@detection_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Deepfake Detection API is running'
    })

@detection_bp.route('/analyze', methods=['POST'])
def analyze_file():
    """Analyze uploaded file for deepfake detection"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file_handler.allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save file
        filepath = file_handler.save_file(file)
        
        if filepath is None:
            return jsonify({'error': 'Failed to save file'}), 500
        
        # Determine file type and process
        if file_handler.is_video(file.filename):
            result = video_processor.predict_video(filepath)
        else:
            result = image_processor.predict_image(filepath)
        
        # Clean up uploaded file
        file_handler.delete_file(filepath)
        
        # Return result
        if result['success']:
            return jsonify({
                'isFake': result['isFake'],
                'confidence': round(result['confidence'], 2),
                'type': result['type'],
                'details': result['details']
            })
        else:
            return jsonify({'error': result['error']}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500