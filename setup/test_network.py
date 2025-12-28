#!/usr/bin/env python3
"""Test network connection untuk Google Sheets"""

import socket
import requests
import time

def test_network():
    print("🌐 NETWORK CONNECTION TEST")
    print("=" * 60)
    
    # Test 1: Internet connectivity
    print("\n1. Testing internet connectivity...")
    try:
        response = requests.get("https://www.google.com", timeout=10)
        print(f"✅ Internet: Connected (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Internet: {e}")
        return False
    
    # Test 2: Google APIs
    print("\n2. Testing Google APIs...")
    try:
        response = requests.get("https://sheets.googleapis.com/$discovery/rest?version=v4", timeout=10)
        print(f"✅ Google APIs: Accessible (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Google APIs: {e}")
        print("   Mungkin ada firewall atau proxy yang memblokir")
    
    # Test 3: DNS resolution
    print("\n3. Testing DNS resolution...")
    try:
        ip = socket.gethostbyname("sheets.googleapis.com")
        print(f"✅ DNS: sheets.googleapis.com -> {ip}")
    except socket.gaierror as e:
        print(f"❌ DNS: {e}")
        return False
    
    # Test 4: Port connectivity
    print("\n4. Testing port connectivity...")
    ports = [80, 443]
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(("sheets.googleapis.com", port))
            if result == 0:
                print(f"✅ Port {port}: Open")
            else:
                print(f"❌ Port {port}: Closed (Error {result})")
            sock.close()
        except Exception as e:
            print(f"❌ Port {port}: {e}")
    
    print("\n" + "=" * 60)
    print("📋 NETWORK DIAGNOSIS:")
    print("Jika Google Sheets gagal tetapi internet OK:")
    print("1. Coba restart aplikasi")
    print("2. Cek firewall/antivirus")
    print("3. Coba koneksi lain (hotspot)")
    print("4. Test dengan: python test_google_sheets.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_network()