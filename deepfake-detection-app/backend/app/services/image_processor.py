import cv2
import numpy as np
# Import TensorFlow dan PyTorch untuk mengecek jenis objek model
import tensorflow as tf
import torch 

class ImageProcessor:
    def __init__(self, face_detector, model):
        self.face_detector = face_detector
        self.model = model
        
        # Tentukan framework model saat inisialisasi
        self.framework = self._determine_framework()

    def _determine_framework(self):
        """Menentukan framework (Keras atau PyTorch) dari objek model yang dimuat."""
        if self.model is None:
            return None
        # Cek apakah objek model adalah Keras Model
        elif isinstance(self.model, tf.keras.Model):
            return 'keras'
        # Cek apakah objek model adalah PyTorch nn.Module
        elif isinstance(self.model, torch.nn.Module):
            # Penting: Set model PyTorch ke mode evaluasi
            self.model.eval() 
            return 'pytorch'
        else:
            return 'unknown'
    
    def predict_image(self, image_path):
        """
        Predict if an image is real or fake using face detection, 
        supporting both Keras/TensorFlow and PyTorch models.
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            
            if image is None:
                return {
                    'success': False,
                    'error': 'Cannot read image',
                    'isFake': None,
                    'confidence': 0.0,
                    'type': 'image'
                }
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Extract face from image
            face = self.face_detector.extract_face_from_frame(image_rgb)
            
            if face is None:
                return {
                    'success': False,
                    'error': 'No face detected in image',
                    'isFake': None,
                    'confidence': 0.0,
                    'type': 'image'
                }
            
            # Preprocess face
            face_processed = self.face_detector.preprocess_face(face)
            
            if face_processed is None:
                return {
                    'success': False,
                    'error': 'Face preprocessing failed',
                    'isFake': None,
                    'confidence': 0.0,
                    'type': 'image'
                }
            
            # --- PREDIKSI BERDASARKAN FRAMEWORK ---
            prediction = 0.0

            if self.framework == 'keras':
                # Keras/TensorFlow: (HWC) -> Normalisasi (0-1) -> Tambah dimensi batch (NHWC)
                face_array = np.expand_dims(face_processed / 255.0, axis=0).astype(np.float32)
                
                # Gunakan metode .predict()
                output = self.model.predict(face_array, verbose=0)
                prediction = float(output[0][0])
            
            elif self.framework == 'pytorch':
                # PyTorch: (HWC) -> Normalisasi (0-1)
                face_normalized = face_processed / 255.0
                
                # Ubah bentuk dan konversi ke Tensor: (H, W, C) -> (C, H, W) -> (1, C, H, W) (NCHW)
                face_tensor = torch.from_numpy(face_normalized).permute(2, 0, 1).unsqueeze(0).float()
                
                # Gunakan panggilan objek model (model(input))
                with torch.no_grad():
                    output = self.model(face_tensor)
                    
                    # Asumsi klasifikasi biner, terapkan Sigmoid untuk probabilitas
                    probabilities = torch.softmax(output, dim=1)
                    prediction_tensor = probabilities[0, 1]
                    prediction = prediction_tensor.item()
            
            else:
                return {
                    'success': False,
                    'error': f"Model not loaded or unrecognized framework: {self.framework}.",
                    'isFake': None,
                    'confidence': 0.0,
                    'type': 'image'
                }

            # Determine label (0 = fake, 1 = real)
            is_fake = prediction <= 0.5
            confidence = (1 - prediction) if is_fake else prediction
            
            return {
                'success': True,
                'isFake': bool(is_fake),
                'confidence': float(confidence * 100),  # Convert to percentage
                'type': 'image',
                'details': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'isFake': None,
                'confidence': 0.0,
                'type': 'image'
            }