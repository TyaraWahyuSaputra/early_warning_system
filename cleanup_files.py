#!/usr/bin/env python3
"""
SCRIPT UNTUK MENGHAPUS FILE AUTH & VISITOR YANG TIDAK DIGUNAKAN
Versi terbaru setelah update app.py

Jalankan: python cleanup_files.py
"""

import os
import shutil
import sys
import time

def print_header(text):
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def check_app_py_before():
    """Cek app.py sebelum cleanup"""
    print_header("🔍 PRE-CHECK: app.py")
    
    if not os.path.exists('app.py'):
        print("❌ ERROR: app.py tidak ditemukan!")
        return False
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cek apakah app.py masih ada referensi ke file yang akan dihapus
    checks = [
        ("VisitorController import", 'from controllers.VisitorController import VisitorController' in content),
        ("AuthController import", 'from controllers.AuthController' in content),
        ("auth_views import", 'from views.auth_views' in content),
        ("visitor_stats import", 'from views.visitor_stats' in content),
    ]
    
    issues = []
    for check_name, exists in checks:
        if exists:
            print(f"⚠️  {check_name} MASIH ADA di app.py")
            issues.append(check_name)
        else:
            print(f"✅ {check_name} sudah dihapus dari app.py")
    
    if issues:
        print(f"\n⚠️  PERINGATAN: {len(issues)} referensi masih ada di app.py")
        print("   Jalankan update_app.py terlebih dahulu!")
        return False
    
    return True

def create_backup():
    """Buat backup file penting"""
    print_header("📦 MEMBUAT BACKUP")
    
    backup_dir = f"backup_{int(time.time())}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        'app.py',
        'controllers/',
        'models/',
        'views/',
        'model_ann.py',
        'gumbel_distribution.py',
        'requirements.txt',
        'flood_system.db'
    ]
    
    backed_up = 0
    for item in files_to_backup:
        if os.path.exists(item):
            if os.path.isdir(item):
                dest = os.path.join(backup_dir, item)
                shutil.copytree(item, dest, dirs_exist_ok=True)
                print(f"✅ Backup folder: {item}/")
            else:
                dest = os.path.join(backup_dir, item)
                shutil.copy2(item, dest)
                print(f"✅ Backup file: {item}")
            backed_up += 1
    
    print(f"\n📊 Total {backed_up} item di-backup ke: {backup_dir}/")
    return backup_dir

def cleanup_auth_system():
    """Hapus file auth system"""
    print_header("🗑️  MENGHAPUS AUTH SYSTEM")
    
    auth_files = [
        'controllers/AuthController.py',
        'models/UserModel.py',
        'views/auth_views.py',
        'schema_users.sql',
    ]
    
    deleted = 0
    for file_path in auth_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Deleted: {file_path}")
                deleted += 1
            except Exception as e:
                print(f"❌ Error: {file_path} - {e}")
        else:
            print(f"ℹ️  Not found: {file_path}")
    
    return deleted

def cleanup_visitor_system():
    """Hapus file visitor system"""
    print_header("🗑️  MENGHAPUS VISITOR SYSTEM")
    
    visitor_files = [
        'controllers/VisitorController.py',
        'models/VisitorModel.py',
        'views/visitor_stats.py',
        'schema_visitor_stats.sql',
    ]
    
    deleted = 0
    for file_path in visitor_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Deleted: {file_path}")
                deleted += 1
            except Exception as e:
                print(f"❌ Error: {file_path} - {e}")
        else:
            print(f"ℹ️  Not found: {file_path}")
    
    return deleted

def cleanup_setup_scripts():
    """Hapus setup scripts yang tidak perlu"""
    print_header("🗑️  MENGHAPUS SETUP SCRIPTS")
    
    setup_files = [
        'setup_google_sheet.py',
        'test_connection.py',
        'test_network.py',
        'final_test.py',
    ]
    
    deleted = 0
    for file_path in setup_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Deleted: {file_path}")
                deleted += 1
            except Exception as e:
                print(f"❌ Error: {file_path} - {e}")
        else:
            print(f"ℹ️  Not found: {file_path}")
    
    return deleted

def verify_deletion():
    """Verifikasi file sudah dihapus"""
    print_header("✅ VERIFIKASI PENGHAPUSAN")
    
    all_files_to_delete = [
        # Auth
        'controllers/AuthController.py',
        'models/UserModel.py',
        'views/auth_views.py',
        'schema_users.sql',
        # Visitor
        'controllers/VisitorController.py',
        'models/VisitorModel.py',
        'views/visitor_stats.py',
        'schema_visitor_stats.sql',
        # Setup
        'setup_google_sheet.py',
        'test_connection.py',
        'test_network.py',
        'final_test.py',
    ]
    
    still_exist = []
    for file_path in all_files_to_delete:
        if os.path.exists(file_path):
            still_exist.append(file_path)
    
    if still_exist:
        print("❌ File berikut masih ada:")
        for file in still_exist:
            print(f"   - {file}")
        return False
    else:
        print("✅ SEMUA file tidak terpakai sudah dihapus!")
        return True

def check_essential_files():
    """Cek file penting masih ada"""
    print_header("🔍 CEK FILE PENTING")
    
    essential_files = [
        'app.py',
        'controllers/FloodReportController.py',
        'controllers/RealTimeDataController.py',
        'models/FloodReportModel.py',
        'models/GoogleSheetsModel.py',
        'views/flood_report_form.py',
        'views/flood_reports_table.py',
        'views/monthly_reports.py',
        'views/prediction_dashboard.py',
        'views/panduan_page.py',
        'model_ann.py',
        'gumbel_distribution.py',
        'requirements.txt',
    ]
    
    missing = []
    for file in essential_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ MISSING: {file}")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  WARNING: {len(missing)} file penting tidak ditemukan!")
        return False
    
    return True

def main():
    print("=" * 60)
    print("🧹 FLOOD WARNING SYSTEM - CLEANUP SCRIPT")
    print("=" * 60)
    print("Versi: 2.0 (Setelah update app.py)")
    print("\n⚠️  PERINGATAN: Script ini akan menghapus file!")
    print("   Pastikan sudah menjalankan update_app.py terlebih dahulu.")
    
    # Konfirmasi
    response = input("\nLanjutkan cleanup? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Cleanup dibatalkan")
        return
    
    # Langkah 1: Pre-check
    if not check_app_py_before():
        print("\n❌ Tidak bisa melanjutkan karena app.py masih ada referensi.")
        print("   Jalankan: python update_app.py terlebih dahulu")
        return
    
    # Langkah 2: Backup
    backup_dir = create_backup()
    
    # Langkah 3: Cleanup
    print_header("🚀 MEMULAI CLEANUP")
    
    total_deleted = 0
    total_deleted += cleanup_auth_system()
    total_deleted += cleanup_visitor_system()
    total_deleted += cleanup_setup_scripts()
    
    # Langkah 4: Verifikasi
    verify_deletion()
    
    # Langkah 5: Cek file penting
    check_essential_files()
    
    print_header("📊 HASIL CLEANUP")
    print(f"✅ Total file dihapus: {total_deleted}")
    print(f"✅ Backup dibuat di: {backup_dir}/")
    print("\n✅ CLEANUP SELESAI!")
    
    print("\n" + "=" * 60)
    print("🚀 LANGKAH SELANJUTNYA:")
    print("1. Test aplikasi: streamlit run app.py")
    print("2. Cek semua menu berfungsi:")
    print("   - Home, Panduan, Lapor Banjir, Catatan Laporan")
    print("   - Prediksi Real-time, Simulasi Banjir")
    print("3. Jika ada error, restore dari backup")
    print("=" * 60)

if __name__ == "__main__":
    main()