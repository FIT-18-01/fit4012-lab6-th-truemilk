#!/usr/bin/env python3
"""Test script to generate success logs."""

import os
import sys
import subprocess
import time
import threading

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_receiver():
    """Run receiver in a thread."""
    env = os.environ.copy()
    env["RECEIVER_HOST"] = "127.0.0.1"
    env["DATA_PORT"] = "6000"
    env["KEY_PORT"] = "6001"
    env["OUTPUT_FILE"] = "sample_output.txt"
    env["RECEIVER_LOG_FILE"] = "logs/receiver_success.log"
    subprocess.run([sys.executable, "receiver.py"], env=env)

def main():
    """Run receiver and sender to generate logs."""
    # Start receiver
    receiver_thread = threading.Thread(target=run_receiver, daemon=True)
    receiver_thread.start()
    
    # Wait for receiver to start listening
    time.sleep(1)
    
    # Run sender
    sender_env = os.environ.copy()
    sender_env["SERVER_IP"] = "127.0.0.1"
    sender_env["DATA_PORT"] = "6000"
    sender_env["KEY_PORT"] = "6001"
    sender_env["MESSAGE"] = "Xin chao FIT4012 - Lab 6 AES Socket"
    sender_env["SENDER_LOG_FILE"] = "logs/sender_success.log"
    subprocess.run([sys.executable, "sender.py"], env=sender_env)
    
    # Wait for receiver to finish
    receiver_thread.join(timeout=5)
    
    print("\n[SUCCESS] Logs generated successfully!")

if __name__ == "__main__":
    main()
