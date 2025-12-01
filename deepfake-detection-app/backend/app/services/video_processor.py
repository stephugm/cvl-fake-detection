import cv2
import numpy as np
import tensorflow as tf
import torch

class VideoProcessor:
    def __init__(self, face_detector, model, frames_per_video=30, frame_skip=3):
        self.face_detector = face_detector
        self.model = model
        self.frames_per_video = frames_per_video
        self.frame_skip = frame_skip
        
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

    
    def extract_frames_from_video(self, video_path):
        """
        Extract frames from a video and detect faces
        """
        faces = []
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            print(f"Error: Cannot open video {video_path}")
            return faces, 0 # Mengembalikan faces dan 0 (frames_processed)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames == 0:
            cap.release()
            return faces, 0 # Mengembalikan faces dan 0 (frames_processed)
        
    
        frame_indices = list(range(0, total_frames, self.frame_skip))
        frames_extracted = len(frame_indices)
        
        
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if ret:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Extract face from frame
                face = self.face_detector.extract_face_from_frame(frame_rgb)
                
                if face is not None:
                    # Preprocess face
                    face_processed = self.face_detector.preprocess_face(face)
                    if face_processed is not None:
                        faces.append(face_processed)
        
        cap.release()
        
        return faces, total_frames, frames_extracted
    
    def predict_video(self, video_path):
        """
        Predict if a video is real or fake using face detection
        """
        try:
            # Mengambil faces dan jumlah total frame yang di-sampling
            faces, total_frames, frames_extracted = self.extract_frames_from_video(video_path)
            total_faces_analyzed = len(faces) 
            
            if frames_extracted == 0:
                return {
                    'success': False,
                    'error': 'No frames could be read from video',
                    'isFake': None,
                    'confidence': 0.0,
                    'type': 'video'
                }
            
            # Hitung persentase wajah yang terdeteksi dari frame yang di-sampling
            percent_face_detected = (total_faces_analyzed / frames_extracted) * 100

            if total_faces_analyzed == 0:
                 return {
                    'success': False,
                    'error': 'No faces detected in extracted frames',
                    'isFake': None,
                    'confidence': 0.0,
                    'type': 'video',
                    'details': {
                        'framesTotal': total_frames,
                        'framesExtracted': frames_extracted, # <-- Total frame yang dicoba dianalisis
                    }
                }
            
            # --- PREDIKSI BERDASARKAN FRAMEWORK ---
            # ... (Logika Prediksi PyTorch/Keras tetap sama, bekerja pada faces) ...
            
            if self.framework == 'keras':
                faces_array = np.array(faces) / 255.0
                predictions = self.model.predict(faces_array, verbose=0)
            
            elif self.framework == 'pytorch':
                # ... (Logika konversi PyTorch) ...
                faces_list = [
                    torch.from_numpy(face / 255.0).permute(2, 0, 1).float() 
                    for face in faces
                ]
                faces_tensor = torch.stack(faces_list)
                with torch.no_grad():
                    outputs = self.model(faces_tensor)
                    if outputs.dim() == 2 and outputs.shape[1] > 1:
                        probabilities = torch.softmax(outputs, dim=1)
                        predictions = probabilities[:, 1].cpu().numpy() 
                    else:
                        predictions = torch.sigmoid(outputs).squeeze().cpu().numpy()
            
            else:
                return {
                    'success': False,
                    'error': f"Model not loaded or unrecognized framework: {self.framework}.",
                    'isFake': None,
                    'confidence': 0.0,
                    'type': 'video'
                }

            # --- ANALISIS PREDIKSI ---
            avg_prediction = float(np.mean(predictions))
            
            # Hitung jumlah frame Real dan Fake (berdasarkan total_faces_analyzed)
            real_count = np.sum(predictions > 0.5)
            fake_count = total_faces_analyzed - real_count
            
            real_percentage = (real_count / total_faces_analyzed) * 100
            fake_percentage = (fake_count / total_faces_analyzed) * 100
            
            # Tentukan label
            is_fake = avg_prediction <= 0.5
            confidence = (1 - avg_prediction) if is_fake else avg_prediction
            
            return {
                'success': True,
                'isFake': bool(is_fake),
                'confidence': float(confidence * 100),
                'type': 'video',
                'details': {
                    'framesTotal': total_frames,
                    'framesExtracted': frames_extracted,
                    'faceDetected': float(percent_face_detected),
                    'realFrames': float(real_percentage),
                    'fakeFrames': float(fake_percentage),
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'isFake': None,
                'confidence': 0.0,
                'type': 'video'
            }