@echo off
chcp 65001 >nul
title 📦 INSTALL DEPENDENCIES SISTEM BANJIR

echo ========================================
echo 📦 INSTALL DEPENDENCIES SISTEM BANJIR
echo ========================================
echo.

echo 1. Meng-upgrade pip...
python -m pip install --upgrade pip
echo ✅ pip upgraded

echo.
echo 2. Menginstall dependencies yang sudah diperbaiki...
pip install streamlit==1.28.0
pip install pandas==2.1.3
pip install numpy==1.25.0
pip install Pillow==10.1.0
pip install gspread==5.11.3
pip install oauth2client==4.1.3
pip install protobuf==3.20.3

echo.
echo 3. Verifikasi install...
python -c "import streamlit; print(f'✅ Streamlit: {streamlit.__version__}')"
python -c "import numpy; print(f'✅ NumPy: {numpy.__version__}')"
python -c "import pandas; print(f'✅ Pandas: {pandas.__version__}')"

echo.
echo ========================================
echo ✅ SEMUA DEPENDENCIES TERINSTALL!
echo.
echo Langkah selanjutnya:
echo   1. Jalankan: run_test.bat
echo   2. Kemudian: streamlit run app.py
echo ========================================
echo.

pause