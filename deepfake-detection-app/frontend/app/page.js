'use client';

import { useState } from 'react';
import axios from 'axios';
import { Upload, Loader, CheckCircle, XCircle, FileImage, FileVideo } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export default function Home() {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [fileType, setFileType] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    /**
     * Menangani perubahan pada input file.
     */
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            // Reset state sebelumnya
            setFile(selectedFile);
            setResult(null);
            setError(null);
            
            // Tentukan tipe file untuk ikon dan preview
            const type = selectedFile.type.startsWith('image/') ? 'image' : 'video';
            setFileType(type);
            
            // Buat preview data URL
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreview(reader.result);
            };
            reader.readAsDataURL(selectedFile);
        }
    };

    /**
     * Mengirim file ke backend untuk analisis deepfake.
     */
    const analyzeFile = async () => {
        if (!file) return;
        
        setAnalyzing(true);
        setError(null);
        setResult(null); 
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            // Kirim permintaan POST ke API backend
            const response = await axios.post(`${API_URL}/api/analyze`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            
            // Simpan hasil analisis
            setResult(response.data);
        } catch (err) {
            // Tangani error dari permintaan
            setError(err.response?.data?.error || 'Terjadi kesalahan saat menganalisis file');
        } finally {
            setAnalyzing(false);
        }
    };

    /**
     * Mereset semua state ke kondisi awal.
     */
    const reset = () => {
        setFile(null);
        setPreview(null);
        setFileType(null);
        setResult(null);
        setError(null);
    };

    // Helper untuk mengubah kunci camelCase menjadi teks yang mudah dibaca
    const getReadableKey = (key) => {
        const mapping = {
            framesTotal: 'Total Frame Video',
            framesExtracted: 'Extracted Frame',
            faceDetected: 'Persentase Wajah Terdeteksi',
            realFrames: 'Persentase Frame Real',
            fakeFrames: 'Persentase Frame Deepfake',
        };
        return mapping[key] || key.replace(/([A-Z])/g, ' $1').trim();
    };

    const displayOrder = [
        'framesTotal',
        'framesExtracted',
        'faceDetected',
        'realFrames',
        'fakeFrames',
    ];

    // --- Komponen Tampilan Hasil Analisis ---
    const ResultDisplay = () => {
        if (!result) return null;

        const isDeepfake = result.isFake;
        // Pastikan confidence dibulatkan untuk tampilan yang rapi
        const confidence = result.confidence.toFixed(2); 
        const isVideoAnalysis = result.type === 'video';


        return (
            <div className="mt-8 pt-6 border-t border-slate-700/50">
                <h2 className="text-3xl font-bold text-white text-center mb-6">
                    Hasil Analisis
                </h2>

                {/* Result Icon */}
                <div className="flex justify-center mb-6">
                    <div className={`w-28 h-28 rounded-full flex items-center justify-center shadow-2xl ${
                        isDeepfake 
                            ? 'bg-gradient-to-br from-red-500 to-red-600' 
                            : 'bg-gradient-to-br from-green-500 to-green-600'
                    }`}>
                        {isDeepfake ? (
                            <XCircle className="w-14 h-14 text-white" />
                        ) : (
                            <CheckCircle className="w-14 h-14 text-white" />
                        )}
                    </div>
                </div>

                <h3 className="text-3xl font-bold text-white text-center mb-2">
                    {isDeepfake ? 'Deepfake Terdeteksi' : 'Asli (Authentic)'}
                </h3>
                <p className="text-center text-slate-400 mb-8 text-xl">
                    Confidence: <span className={`font-extrabold ${isDeepfake ? 'text-red-400' : 'text-green-400'}`}>{confidence}%</span>
                </p>

                {/* Tampilkan DETAIL METRIK hanya JIKA analisis adalah VIDEO */}
                {isVideoAnalysis && (
                    <div className="space-y-4 mb-6">
                        <h4 className="text-lg font-semibold text-slate-300">Detail Metrik Video:</h4>
                        
                        {displayOrder.map((key) => {
                            // Ambil nilai dari objek result.details
                            const value = result.details[key];

                            // Pastikan kunci ada dan nilainya tidak null
                            if (value === undefined || value === null) return null;

                            const readableKey = getReadableKey(key);
                            const isCount = key.startsWith('frames');
                            
                            // Tampilan nilai: bilangan bulat untuk hitungan, % untuk persentase
                            const displayValue = isCount ? Math.round(value) : value.toFixed(2) + '%';
                            // Progress bar hanya untuk persentase
                            const progressValue = isCount ? null : value; 
                            
                            return (
                                <div key={key} className="bg-slate-900/30 rounded-lg p-4 border border-slate-700/50">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="text-slate-300">{readableKey}</span>
                                        <span className="text-white font-semibold">{displayValue}</span>
                                    </div>
                                    
                                    {progressValue !== null && (
                                        <div className="w-full bg-slate-700 rounded-full h-2">
                                            <div
                                                className="bg-gradient-to-r from-cyan-400 to-blue-500 h-2 rounded-full transition-all duration-500"
                                                style={{ width: `${progressValue}%` }}
                                            />
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                )}
                
                {/* Action Button (Tombol Reset) */}
                <button
                    onClick={reset}
                    className="w-full mt-6 py-3 bg-slate-700/50 hover:bg-slate-700 text-slate-300 font-medium rounded-lg transition-colors"
                >
                    Reset
                </button>
            </div>
        );
    };
    // --- Akhir Komponen Tampilan Hasil Analisis ---

    return (
        <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
            <div className="w-full max-w-2xl">
                {/* Logo */}
                <div className="text-center mb-8">
                    <h1 className="text-5xl font-bold text-white mb-2">Deepfake</h1>
                    <p className="text-slate-400">AI-Powered Detection System</p>
                </div>

                {/* Card Container */}
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl shadow-2xl border border-slate-700/50 overflow-hidden p-8">
                    {/* Avatar/Icon */}
                    <div className="flex justify-center mb-8">
                        <div className="w-32 h-32 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full flex items-center justify-center shadow-lg">
                            {fileType === 'image' ? (
                                <FileImage className="w-16 h-16 text-white" />
                            ) : fileType === 'video' ? (
                                <FileVideo className="w-16 h-16 text-white" />
                            ) : (
                                <Upload className="w-16 h-16 text-white" />
                            )}
                        </div>
                    </div>

                    <h2 className="text-3xl font-bold text-white text-center mb-8">
                        Upload File
                    </h2>

                    {/* File Upload Area */}
                    <div className="mb-6">
                        <label className="block text-slate-300 text-sm mb-2">
                            File (Gambar atau Video) <span className="text-red-400">*</span>
                        </label>
                        <div className="relative">
                            <input
                                type="file"
                                accept="image/*,video/*"
                                onChange={handleFileChange}
                                className="hidden"
                                id="file-upload"
                            />
                            <label
                                htmlFor="file-upload"
                                className="block w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-slate-300 cursor-pointer hover:bg-slate-700/70 transition-colors"
                            >
                                {file ? file.name : 'Pilih gambar atau video...'}
                            </label>
                        </div>
                    </div>

                    {/* Preview */}
                    {preview && (
                        <div className="mb-6">
                            <label className="block text-slate-300 text-sm mb-2">Preview</label>
                            <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700">
                                {fileType === 'image' ? (
                                    <img src={preview} alt="Preview" className="w-full h-64 object-contain rounded" />
                                ) : (
                                    <video src={preview} controls className="w-full h-64 rounded" />
                                )}
                            </div>
                        </div>
                    )}

                    {/* Error Message */}
                    {error && (
                        <div className="mb-6 bg-red-500/20 border border-red-500 rounded-lg p-4">
                            <p className="text-red-200 text-sm">{error}</p>
                        </div>
                    )}

                    {/* Analyze Button */}
                    <button
                        onClick={analyzeFile}
                        disabled={!file || analyzing}
                        className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 disabled:from-slate-600 disabled:to-slate-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all shadow-lg hover:shadow-cyan-500/50 disabled:shadow-none flex items-center justify-center gap-2"
                    >
                        {analyzing ? (
                            <>
                                <Loader className="w-5 h-5 animate-spin" />
                                Menganalisis...
                            </>
                        ) : (
                            'Analisis'
                        )}
                    </button>

                    {/* Tombol Reset File yang diunggah jika belum dianalisis */}
                    {file && !analyzing && !result && (
                        <button
                            onClick={reset}
                            className="w-full mt-3 py-3 bg-slate-700/50 hover:bg-slate-700 text-slate-300 font-medium rounded-lg transition-colors"
                        >
                            Batalkan dan Reset
                        </button>
                    )}

                    {/* Tampilkan Hasil Analisis */}
                    <ResultDisplay />

                </div>

                {/* Footer Info */}
                <div className="mt-6 text-center">
                    <p className="text-slate-500 text-sm">
                        CVL Group 4
                    </p>
                </div>
            </div>
        </main>
    );
}