import re

# Baca file app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Ganti semua print() dengan sys.stderr.write()
pattern = r'print\((.*?)\)'
replacement = r'sys.stderr.write(str(\1) + "\\n"); sys.stderr.flush()'

# Ganti print() kecuali yang ada di string atau comment
fixed_content = re.sub(pattern, replacement, content)

# Juga ganti traceback.print_exc()
fixed_content = fixed_content.replace('traceback.print_exc()', 'traceback.print_exc(file=sys.stderr)')

# Simpan backup dan file baru
with open('app.py.backup', 'w', encoding='utf-8') as f:
    f.write(content)
    
with open('app_fixed.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Fixed! File baru: app_fixed.py")
print("✅ Backup: app.py.backup")