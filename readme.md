# CVL Fake Detection

Repository ini berisi kode dan eksperimen untuk proyek deteksi deepfake (gambar & video). Proyek menggabungkan beberapa komponen:

- Backend: API Flask untuk upload dan deteksi (`code/deepfake-detection-app/backend`).
- Frontend: antarmuka Next.js untuk demo/tes (`code/deepfake-detection-app/frontend`).
- Eksperimen & model: notebook dan model terlatih di folder `code/experiment`.

Penekanan utama:
- Ekstraksi wajah/deteksi wajah menggunakan ResNet/face detector.
- Klasifikasi deepfake pada frame/video menggunakan model berbasis EfficientNet/ResNet.

## Struktur Proyek (ringkas)

- `code/deepfake-detection-app/backend` — Flask app, layanan deteksi, utilitas, dan dependensi (`requirements.txt`).
- `code/deepfake-detection-app/frontend` — Next.js frontend (scripts di `package.json`).
- `code/experiment` — notebook pelatihan, dan evaluasi.

## Resources

Link ke dokumen akhir dan laporan terkait:

- Final Project PPT: `CVL_Group_4_Final_Project.pptx`
- Laporan: `docs/Video_and_Image_Manipulation_Detection_Based_on_ResNet_and_EfficientNet.pdf`

## Eksperimen & Model

- Notebook pelatihan dan evaluasi ada di `code/experiment`.
- Model terlatih (contoh) tersedia di `https://drive.google.com/drive/folders/1-lxbnWmj4mC-bX0Md1L89dYt2lrDdJbK?usp=sharing` (mis. `ResNet50_final.keras`).

Untuk mengeksekusi atau menyesuaikan eksperimen, buka notebook yang relevan dan ikuti cell dokumentasi di dalamnya.

## Persyaratan

- Python 3.8+ untuk backend/eksperimen.
- Node.js 18+ / npm untuk frontend.
- GPU direkomendasikan untuk pelatihan/penilaian model, tetapi inferensi CPU dapat dijalankan untuk pengujian kecil.

## Menjalankan Backend (PowerShell)

1. Buat dan aktifkan virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instal dependensi:

```powershell
pip install -r code\deepfake-detection-app\backend\requirements.txt
```

3. Jalankan server Flask:

```powershell
cd code\deepfake-detection-app\backend
python run.py
```

Server akan berjalan pada `http://0.0.0.0:5000` (default). Endpoint deteksi tersedia di route yang diimplementasikan pada `app/routes/detection.py`.

## Menjalankan Frontend

1. Masuk ke folder frontend dan instal dependensi:

```powershell
cd code\deepfake-detection-app\frontend
npm install
```

2. Jalankan mode development:

```powershell
npm run dev
```

Frontend akan aktif pada `http://localhost:3000` (default Next.js).

## Penggunaan (ringkas)

1. Jalankan backend.
2. Copy model ke `code\deepfake-detection-app\backend\app\models`
3. Jalankan frontend (opsional, bisa gunakan curl/postman untuk API).
4. Upload video/gambar melalui antarmuka atau endpoint API.
5. Hasil deteksi akan dikembalikan oleh backend (biasanya berupa label/score dan metadata frame).
