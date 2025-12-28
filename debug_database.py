import sqlite3
import os
from datetime import datetime

def debug_database():
    print("🔧 DEBUG DATABASE STARTED")
    
    # Hapus database lama jika ada
    if os.path.exists('flood_system.db'):
        os.remove('flood_system.db')
        print("🗑️ Database lama dihapus")
    
    try:
        # Test koneksi database
        conn = sqlite3.connect('flood_system.db')
        cursor = conn.cursor()
        print("✅ Koneksi database berhasil")
        
        # Buat tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flood_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                flood_height TEXT NOT NULL,
                reporter_name TEXT NOT NULL,
                reporter_phone TEXT,
                photo_path TEXT,
                ip_address TEXT,
                report_date DATE DEFAULT CURRENT_DATE,
                report_time TIME DEFAULT CURRENT_TIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        print("✅ Tabel flood_reports berhasil dibuat")
        
        # Test insert data
        test_data = [
            ('Jl. Test 123', 'Setinggi lutut', 'Test User 1', '08123456789', None, '127.0.0.1'),
            ('Jl. Contoh 456', 'Setinggi betis', 'Test User 2', None, None, '127.0.0.1')
        ]
        
        for address, flood_height, reporter_name, phone, photo, ip in test_data:
            cursor.execute('''
                INSERT INTO flood_reports (address, flood_height, reporter_name, reporter_phone, photo_path, ip_address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (address, flood_height, reporter_name, phone, photo, ip))
            print(f"✅ Data test inserted: {reporter_name}")
        
        conn.commit()
        print("✅ Commit berhasil")
        
        # Test read data
        cursor.execute('SELECT COUNT(*) FROM flood_reports')
        count = cursor.fetchone()[0]
        print(f"✅ Jumlah data dalam database: {count}")
        
        # Tampilkan semua data
        cursor.execute('SELECT * FROM flood_reports')
        rows = cursor.fetchall()
        print("📊 Data dalam database:")
        for row in rows:
            print(f"  - ID: {row[0]}, Alamat: {row[1]}, Pelapor: {row[3]}")
        
        conn.close()
        print("✅ Debug database selesai - SEMUA TEST BERHASIL")
        return True
        
    except Exception as e:
        print(f"❌ ERROR dalam debug database: {e}")
        return False

if __name__ == "__main__":
    debug_database()