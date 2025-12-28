#!/usr/bin/env python3
"""
FIX UNICODE ENCODING ISSUE ON WINDOWS
Jalankan: python fix_encoding.py
"""

import os
import re
import sys

def fix_app_py_encoding():
    """Fix encoding issue in app.py"""
    
    print("🔧 Fixing encoding issue in app.py...")
    
    if not os.path.exists('app.py'):
        print("❌ app.py not found!")
        return False
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace problematic emoji with text
    replacements = [
        ('🔍', '[INFO]'),
        ('🔄', '[INIT]'),
        ('✅', '[OK]'),
        ('❌', '[ERROR]'),
        ('⚠️', '[WARNING]'),
        ('📂', '[DB]'),
        ('📝', '[FORM]'),
        ('📊', '[DASHBOARD]'),
        ('🧮', '[CALCULATOR]'),
        ('📘', '[GUIDE]'),
        ('🌊', ''),
    ]
    
    original_content = content
    for emoji, replacement in replacements:
        content = content.replace(emoji, replacement)
    
    if content != original_content:
        # Backup original
        with open('app.py.backup', 'w', encoding='utf-8') as f:
            f.write(original_content)
        print("✅ Created backup: app.py.backup")
        
        # Write fixed version
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed app.py encoding")
        
        # Show what was changed
        changes = sum(1 for old, new in replacements if old in original_content)
        print(f"✅ Replaced {changes} emoji characters")
        return True
    else:
        print("ℹ️ No emoji found to replace")
        return False

def add_windows_fix():
    """Add Windows encoding fix to app.py"""
    
    print("\n🔧 Adding Windows encoding fix...")
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if fix already exists
    if 'sys.stdout = io.TextIOWrapper' in content:
        print("✅ Windows encoding fix already exists")
        return False
    
    # Find imports section
    import_section = """import streamlit as st
import streamlit.components.v1 as components
import sys
import os
import traceback
import time"""
    
    new_imports = """import streamlit as st
import streamlit.components.v1 as components
import sys
import os
import traceback
import time
import io"""
    
    if import_section in content:
        content = content.replace(import_section, new_imports)
        
        # Add Windows fix after imports
        windows_fix = """
# ==================== WINDOWS ENCODING FIX ====================
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
"""
        
        # Insert after imports
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'import io' in line:
                insert_position = i + 1
                lines.insert(insert_position, windows_fix)
                content = '\n'.join(lines)
                break
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Added Windows encoding fix")
        return True
    else:
        print("⚠️ Could not find import section")
        return False

def test_fix():
    """Test the fix"""
    print("\n🧪 Testing the fix...")
    
    try:
        result = os.system(f'"{sys.executable}" -c "import app"')
        if result == 0:
            print("✅ Fix successful! app.py can now be imported")
            return True
        else:
            print("❌ Fix might not have worked")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 FIX WINDOWS UNICODE ENCODING ISSUE")
    print("=" * 60)
    print("Masalah: Emoji tidak bisa di-encode di Windows (cp1252)")
    print("\nLangkah perbaikan:")
    print("1. Ganti emoji dengan text")
    print("2. Tambah Windows encoding fix")
    print("3. Test perbaikan")
    
    print("\n" + "=" * 60)
    
    # Step 1: Replace emoji
    if fix_app_py_encoding():
        print("\n✅ Step 1: Emoji replaced")
    else:
        print("\n⚠️ Step 1: No changes needed")
    
    # Step 2: Add Windows fix
    if add_windows_fix():
        print("✅ Step 2: Windows encoding fix added")
    else:
        print("ℹ️ Step 2: Windows fix already exists or not needed")
    
    # Step 3: Test
    if test_fix():
        print("\n🎉 PERBAIKAN BERHASIL!")
        print("\n🚀 Sekarang bisa jalankan:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️ Mungkin masih ada masalah")
        print("Coba manual: python -c 'import app'")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()