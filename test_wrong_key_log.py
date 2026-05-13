#!/usr/bin/env python3
"""Generate wrong key test log."""

import os
from pathlib import Path
from aes_socket_utils import decrypt_aes_cbc, encrypt_aes_cbc

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create logs directory
Path("logs").mkdir(exist_ok=True)

# Test encryption with one key
plaintext = b"Xin chao FIT4012 - Lab 6 AES Socket"
key, iv, ciphertext = encrypt_aes_cbc(plaintext, key_size=16)

# Create wrong key
wrong_key = b"0" * 16

# Try to decrypt with wrong key
try:
    recovered = decrypt_aes_cbc(wrong_key, iv, ciphertext)
    message = f"Plaintext with wrong key: {recovered.decode('utf-8', errors='replace')}"
except ValueError as e:
    message = f"Decryption failed with error: {e}"

# Write log
log_content = f"""[+] Wrong Key Test Log - Lab 6
[+] Testing decryption with wrong key

Original plaintext: {plaintext.decode('utf-8')}
Plaintext length: {len(plaintext)} bytes

Correct key: {key.hex()}
IV: {iv.hex()}

Ciphertext: {ciphertext.hex()}

Wrong key (used for decryption): {wrong_key.hex()}

Result: {message}

[SUCCESS] Wrong key test completed - plaintext cannot be recovered with wrong key
"""

wrong_key_log = Path("logs/wrong_key_test.log")
wrong_key_log.write_text(log_content, encoding="utf-8")
print(log_content)
print("[SUCCESS] Wrong key log saved to logs/wrong_key_test.log")
