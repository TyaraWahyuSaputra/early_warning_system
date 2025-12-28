import sqlite3
from datetime import datetime

def debug_limit():
    """Debug limit problem"""
    print("="*60)
    print("🔧 DEBUG LIMIT PROBLEM")
    print("="*60)
    
    try:
        # Hapus database lama
        import os
        if os.path.exists('flood_system.db'):
            os.remove('flood_system.db')
            print("🗑️ Deleted old database")
        
        # Buat database baru
        from models.FloodReportModel import FloodReportModel
        model = FloodReportModel()
        
        conn = sqlite3.connect('flood_system.db')
        cursor = conn.cursor()
        
        print("\n📋 TABLE STRUCTURE:")
        cursor.execute("PRAGMA table_info(flood_reports)")
        for col in cursor.fetchall():
            print(f"  {col[1]} ({col[2]})")
        
        print("\n📊 TEST 1: Insert 1 report")
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO flood_reports 
            (address, flood_height, reporter_name, ip_address, report_date)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Jl. Test 1', 'Setinggi lutut', 'User 1', 'test_user_123', today))
        conn.commit()
        
        print("✅ Inserted 1 report")
        
        print("\n📊 TEST 2: Count reports for IP")
        cursor.execute('''
            SELECT COUNT(*) FROM flood_reports 
            WHERE ip_address = ? AND report_date = ?
        ''', ('test_user_123', today))
        
        count = cursor.fetchone()[0]
        print(f"✅ Count for today: {count}")
        
        print("\n📊 TEST 3: Show all data")
        cursor.execute('SELECT * FROM flood_reports')
        rows = cursor.fetchall()
        for row in rows:
            print(f"  ID:{row[0]} | IP:{row[6]} | Date:{row[7]} | Address:{row[1]}")
        
        conn.close()
        
        print("\n" + "="*60)
        print("🎯 TEST MANUAL:")
        print("1. Buka aplikasi (streamlit run app.py)")
        print("2. Submit 1 form laporan")
        print("3. Lihat output di terminal VS Code")
        print("4. Submit form kedua - harus berhasil")
        print("5. Ulangi sampai 10 kali")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_limit()