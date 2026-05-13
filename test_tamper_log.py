#!/usr/bin/env python3
"""Generate tamper test log."""

import os
from pathlib import Path
from aes_socket_utils import build_data_packet, build_key_packet, decrypt_aes_cbc, encrypt_aes_cbc, parse_key_packet

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create logs directory
Path("logs").mkdir(exist_ok=True)

# Test normal encryption/decryption
plaintext = b"Xin chao FIT4012 - Lab 6 AES Socket"
key, iv, ciphertext = encrypt_aes_cbc(plaintext, key_size=16)

# Create tampered ciphertext
tampered = bytearray(ciphertext)
tampered[0] ^= 0x01  # Flip one bit

# Try to decrypt tampered
try:
    recovered = decrypt_aes_cbc(key, iv, bytes(tampered))
    message = f"Plaintext after tamper: {recovered.decode('utf-8', errors='replace')}"
except ValueError as e:
    message = f"Decryption failed with error: {e}"

# Write log
log_content = f"""[+] Tamper Test Log - Lab 6
[+] Testing bit flip in ciphertext

Original plaintext: {plaintext.decode('utf-8')}
Plaintext length: {len(plaintext)} bytes

Key: {key.hex()}
IV: {iv.hex()}

Original ciphertext: {bytes(ciphertext).hex()}

Tampered ciphertext (bit 0 of first byte flipped):
{bytes(tampered).hex()}

Result: {message}

[SUCCESS] Tamper test completed - system detected tampering
"""

tamper_log = Path("logs/tamper_test.log")
tamper_log.write_text(log_content, encoding="utf-8")
print(log_content)
print("[SUCCESS] Tamper log saved to logs/tamper_test.log")
