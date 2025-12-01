# Branch: Pengembangan EfficientNet-B7 untuk Deteksi Deepfake

## Deskripsi

Branch ini difokuskan pada **pengembangan model EfficientNet-B7** untuk mendeteksi video deepfake.  
Dataset yang digunakan adalah **CelebDFv2**.

---

## Fitur

- Deteksi deepfake menggunakan **EfficientNet-B7**.
- Ekstraksi wajah menggunakan **MTCNN (Facenet-PyTorch)**.
- Evaluasi performa menggunakan **accuracy, F1-score, ROC-AUC, dan confusion matrix**.
- Melputi cross-dataset evaluation dengan data validasi dari dataset **FaceForensic++**.

---

## Persyaratan

Library Python yang digunakan dapat diinstall melalui `pip` dengan `requirements.txt` yang sudah disediakan.

```bash
pip install -r requirements.txt
```

---

## Credit

Pengembangan kode dibantu oleh ChatGPT milik OpenAI.
