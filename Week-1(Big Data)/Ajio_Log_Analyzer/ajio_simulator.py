import socket
import threading
import random
import time
from datetime import datetime

# Simulated Ajio regional servers and their ports
BRANCHES = [
    ("ajio-chennai", 8001),
    ("ajio-mumbai", 8002),
    ("ajio-bengaluru", 8003),
]

LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

# Ajio-specific e-commerce events
MESSAGE_TEMPLATES = {
    "INFO": [
        "Order#{oid} placed successfully for Men's Wear",
        "Payment for Order#{oid} received",
        "User added Item#{oid} to shopping cart",
        "Order#{oid} dispatched from warehouse",
    ],
    "WARNING": [
        "Item#{oid} stock running critically low",
        "High traffic detected on Winter Collection",
        "Delivery partner delayed for Order#{oid}",
    ],
    "ERROR": [
        "Payment gateway timeout for Order#{oid}",
        "Failed to load inventory for Category ID {oid}",
        "Database connection lost while updating Order#{oid}",
    ],
    "DEBUG": [
        "Cache miss for User profile data",
        "Retrying image load for Product#{oid}",
    ],
}

def build_log_line(branch_name):
    level = random.choice(LEVELS)
    oid = random.randint(1000, 9999)
    message = random.choice(MESSAGE_TEMPLATES[level]).format(oid=oid)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} | {level} | {branch_name} | {message}\n"

def handle_client(conn, branch_name):
    print(f"[{branch_name}] Harvester connected, streaming Ajio logs...")
    try:
        while True:
            line = build_log_line(branch_name)
            conn.sendall(line.encode("utf-8"))
            time.sleep(random.uniform(0.05, 0.4))

            if random.random() < 0.05:
                conn.sendall(b"CORRUPTED_PACKET_DATA\n")
    except (BrokenPipeError, ConnectionResetError):
        print(f"[{branch_name}] Harvester disconnected.")
    finally:
        conn.close()

def run_branch_server(branch_name, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("127.0.0.1", port))
    server_sock.listen(1)
    print(f"[{branch_name}] Listening on port {port}...")

    while True:
        conn, addr = server_sock.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(conn, branch_name), daemon=True
        )
        client_thread.start()

if __name__ == "__main__":
    for name, port in BRANCHES:
        t = threading.Thread(target=run_branch_server, args=(name, port), daemon=True)
        t.start()
    
    print("\nAll Ajio simulated servers are up. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down Ajio simulator.")