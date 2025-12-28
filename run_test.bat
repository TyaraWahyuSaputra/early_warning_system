@echo off
chcp 65001 >nul
title 🧪 TEST SISTEM BANJIR - VS CODE

echo ========================================
echo 🧪 TEST SISTEM BANJIR - VS CODE
echo ========================================
echo.

echo 1. Membersihkan environment...
if exist __pycache__ rmdir /s /q __pycache__
if exist models\__pycache__ rmdir /s /q models\__pycache__
if exist controllers\__pycache__ rmdir /s /q controllers\__pycache__
if exist views\__pycache__ rmdir /s /q views\__pycache__
del /q *.pyc 2>nul
del /q models\*.pyc 2>nul
del /q controllers\*.pyc 2>nul
del /q views\*.pyc 2>nul
echo ✅ Cache cleaned

echo.
echo 2. Membersihkan database lama...
if exist flood_system.db (
    del flood_system.db
    echo ✅ Database lama dihapus
) else (
    echo ℹ️ Database tidak ditemukan
)

echo.
echo 3. Membersihkan folder uploads...
if exist uploads (
    rmdir /s /q uploads
    echo ✅ Folder uploads dihapus
) else (
    echo ℹ️ Folder uploads tidak ditemukan
)

echo.
echo 4. Membuat struktur folder...
mkdir models 2>nul
mkdir controllers 2>nul
mkdir views 2>nul
mkdir uploads 2>nul
echo ✅ Folder structure created

echo.
echo 5. Menjalankan test sistem...
python test_system.py

echo.
echo ========================================
echo 🚀 SISTEM SIAP DIJALANKAN!
echo.
echo Untuk menjalankan aplikasi:
echo   streamlit run app.py
echo.
echo Setelah aplikasi berjalan:
echo 1. Buka http://localhost:8501
echo 2. Pilih "Lapor Banjir"
echo 3. Isi form dan submit
echo 4. Cek "Laporan Harian" untuk verifikasi
echo ========================================
echo.

pause