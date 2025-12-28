import sys
import os

# Test print vs sys.stderr.write
print("TEST 1: Normal print - mungkin error")
sys.stdout.flush()

sys.stderr.write("TEST 2: stderr write - pasti aman\n")
sys.stderr.flush()

print("="*50)
print("Jika hanya TEST 2 yang muncul, berarti FIX berhasil!")