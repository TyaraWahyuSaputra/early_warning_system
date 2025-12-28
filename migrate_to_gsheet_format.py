#!/usr/bin/env python3
"""
Script untuk migrasi database ke format Google Sheets
Lakukan SEBELUM update kode aplikasi
"""

import sqlite3
import os
import shutil
from datetime import datetime
import pytz

def backup_database():
    """Backup database sebelum migrasi"""
    if os.path.exists('flood_system.db'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'flood_system_backup_{timestamp}.db'
        shutil.copy2('flood_system.db', backup_name)
        print(f"✅ Database backed up to: {backup_name}")
        return backup_name
    return None

def migrate_database():
    """Migrate database ke format Google Sheets"""
    
    print("=" * 60)
    print("🔄 MIGRATING DATABASE TO GOOGLE SHEETS FORMAT")
    print("=" * 60)
    
    # Backup dulu
    backup_file = backup_database()
    if not backup_file:
        print("⚠️ No database found, creating new one")
    
    try:
        conn = sqlite3.connect('flood_system.db')
        cursor = conn.cursor()
        
        # 1. Cek apakah tabel lama ada
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flood_reports'")
        if not cursor.fetchone():
            print("❌ Tabel flood_reports tidak ditemukan")
            return False
        
        # 2. Cek struktur lama
        cursor.execute("PRAGMA table_info(flood_reports)")
        old_columns = cursor.fetchall()
        print("\n📋 Current table structure:")
        for col in old_columns:
            print(f"  {col[1]} ({col[2]})")
        
        # 3. Buat tabel baru dengan struktur Google Sheets
        print("\n🔄 Creating new table structure...")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flood_reports_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "Timestamp" TEXT,
                "Alamat" TEXT NOT NULL,
                "Tinggi Banjir" TEXT NOT NULL,
                "Nama Pelapor" TEXT NOT NULL,
                "No HP" TEXT,
                "IP Address" TEXT,
                "Photo URL" TEXT,
                "Status" TEXT DEFAULT 'pending',
                report_date DATE,
                report_time TIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 4. Mapping kolom lama ke baru
        print("📊 Migrating data with column mapping...")
        
        # Coba dengan mapping yang mungkin
        try:
            cursor.execute('''
                INSERT INTO flood_reports_new 
                (id, "Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", 
                "No HP", "IP Address", "Photo URL", "Status",
                report_date, report_time, created_at)
                SELECT 
                    id,
                    timestamp as "Timestamp",
                    address as "Alamat",
                    flood_height as "Tinggi Banjir",
                    reporter_name as "Nama Pelapor",
                    reporter_phone as "No HP",
                    ip_address as "IP Address",
                    photo_path as "Photo URL",
                    COALESCE(status, 'pending') as "Status",
                    report_date,
                    report_time,
                    created_at
                FROM flood_reports
            ''')
        except sqlite3.OperationalError as e:
            print(f"⚠️ Standard mapping failed: {e}")
            print("🔄 Trying alternative mapping...")
            
            # Coba mapping minimal
            cursor.execute('''
                INSERT INTO flood_reports_new 
                ("Alamat", "Tinggi Banjir", "Nama Pelapor")
                SELECT 
                    address,
                    flood_height,
                    reporter_name
                FROM flood_reports
            ''')
        
        # 5. Hapus tabel lama dan rename baru
        cursor.execute("DROP TABLE flood_reports")
        cursor.execute("ALTER TABLE flood_reports_new RENAME TO flood_reports")
        
        conn.commit()
        
        # 6. Verifikasi
        cursor.execute("SELECT COUNT(*) FROM flood_reports")
        count = cursor.fetchone()[0]
        
        cursor.execute("PRAGMA table_info(flood_reports)")
        new_columns = cursor.fetchall()
        
        print("\n✅ Migration successful!")
        print(f"📊 Total records migrated: {count}")
        
        print("\n📋 New table structure:")
        for col in new_columns:
            print(f"  {col[1]} ({col[2]})")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("🎉 DATABASE MIGRATION COMPLETE!")
        print(f"📁 Backup saved as: {backup_file}")
        print("\nKolom sekarang sesuai Google Sheets:")
        print("  A: Timestamp      B: Alamat")
        print("  C: Tinggi Banjir  D: Nama Pelapor")
        print("  E: No HP          F: IP Address")
        print("  G: Photo URL      H: Status")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        
        # Restore dari backup
        if backup_file and os.path.exists(backup_file):
            print(f"\n⚠️ Restoring from backup: {backup_file}")
            shutil.copy2(backup_file, 'flood_system.db')
            print("✅ Database restored from backup")
        
        import traceback
        traceback.print_exc()
        return False

def test_migration():
    """Test bahwa migrasi berhasil"""
    print("\n🧪 TESTING MIGRATION")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('flood_system.db')
        cursor = conn.cursor()
        
        # Insert test data
        cursor.execute('''
            INSERT INTO flood_reports 
            ("Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", 
            "No HP", "IP Address", "Photo URL", "Status",
            report_date, report_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            '2024-01-15 19:44:00',
            'Jl. Test Migrasi',
            'Setinggi lutut',
            'Test User',
            '08123456789',
            '192.168.1.100',
            'test.jpg',
            'pending',
            '2024-01-15',
            '19:44:00'
        ))
        
        conn.commit()
        
        # Verify
        cursor.execute('SELECT * FROM flood_reports ORDER BY id DESC LIMIT 1')
        latest = cursor.fetchone()
        
        cursor.execute("PRAGMA table_info(flood_reports)")
        columns = [col[1] for col in cursor.fetchall()]
        
        print("\n✅ Test data inserted:")
        for col_name, value in zip(columns, latest):
            print(f"  {col_name}: {value}")
        
        conn.close()
        
        print("\n🎉 Migration test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Jalankan migrasi
    if migrate_database():
        test_migration()
        
    print("\n📌 NEXT STEPS:")
    print("1. Update semua file Python dengan versi baru")
    print("2. Jalankan aplikasi: streamlit run app.py")
    print("3. Test submit laporan baru")
    print("4. Cek data di SQLite dan Google Sheets")