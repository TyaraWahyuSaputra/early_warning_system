import sqlite3
import os
import sys

def check_database():
    db_path = 'flood_system.db'
    
    print("=" * 60)
    print("DATABASE DIAGNOSTIC CHECK")
    print("=" * 60)
    
    # 1. Cek file existence
    if not os.path.exists(db_path):
        print(f"❌ ERROR: File '{db_path}' NOT FOUND")
        print(f"📂 Current directory: {os.getcwd()}")
        print(f"📋 Files in directory:")
        for f in os.listdir('.'):
            print(f"  - {f}")
        return False
    
    print(f"✅ File exists: {db_path}")
    print(f"📊 File size: {os.path.getsize(db_path)} bytes")
    
    # 2. Cek koneksi database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ Database connection successful")
        
        # 3. Cek tabel
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️ WARNING: No tables found in database")
        else:
            print(f"📁 Tables found: {len(tables)}")
            for table in tables:
                table_name = table[0]
                print(f"\n  Table: {table_name}")
                
                # Cek struktur tabel
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"    Columns: {len(columns)}")
                for col in columns:
                    print(f"      - {col[1]} ({col[2]})")
                
                # Cek jumlah data
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    Total rows: {count}")
                
                # Tampilkan sample data
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                    samples = cursor.fetchall()
                    print(f"    Sample data (first 2 rows):")
                    for i, sample in enumerate(samples):
                        print(f"      Row {i+1}: {sample}")
        
        conn.close()
        print("\n" + "=" * 60)
        print("✅ DATABASE CHECK COMPLETE - ALL SYSTEMS GO!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    check_database()