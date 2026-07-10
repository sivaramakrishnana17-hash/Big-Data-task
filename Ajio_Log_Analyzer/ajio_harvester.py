import socket
import threading
import re
import struct
import os
import time
from collections import defaultdict

BRANCHES = [
    ("ajio-chennai", 8001),
    ("ajio-mumbai", 8002),
    ("ajio-bengaluru", 8003),
]

HOST = "127.0.0.1"
PARTITION_DIR = "ajio_partitions"

# Regex to validate: YYYY-MM-DD HH:MM:SS | LEVEL | service | message
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\|\s*"
    r"(?P<level>INFO|WARNING|ERROR|DEBUG)\s*\|\s*"
    r"(?P<service>[\w\-]+)\s*\|\s*"
    r"(?P<message>.+)$"
)

LEVEL_CODE = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

partition_files = {}
partition_locks = defaultdict(threading.Lock)
partitions_master_lock = threading.Lock()
stats_lock = threading.Lock()
stats = defaultdict(int)

def get_partition_file(service, level):
    key = (service, level)
    with partitions_master_lock:
        if key not in partition_files:
            os.makedirs(PARTITION_DIR, exist_ok=True)
            filename = os.path.join(PARTITION_DIR, f"{service}_{level}.bin")
            partition_files[key] = open(filename, "ab")
        return partition_files[key]

def encode_record(timestamp, level, service, message):
    ts_bytes = timestamp.encode("ascii").ljust(19, b" ")[:19]
    level_byte = LEVEL_CODE[level]
    service_bytes = service.encode("utf-8")
    message_bytes = message.encode("utf-8")

    header = struct.pack("!19sBH", ts_bytes, level_byte, len(service_bytes))
    mid = struct.pack("!H", len(message_bytes))
    return header + service_bytes + mid + message_bytes

def write_payload(record):
    binary_record = encode_record(
        record["timestamp"], record["level"], record["service"], record["message"]
    )
    length_prefix = struct.pack("!I", len(binary_record))
    
    key = (record["service"], record["level"])
    f = get_partition_file(record["service"], record["level"])
    with partition_locks[key]:
        f.write(length_prefix + binary_record)
        f.flush()

def process_line(raw_line, branch_name):
    match = LOG_PATTERN.match(raw_line)
    if not match:
        with stats_lock:
            stats[(branch_name, "REJECTED")] += 1
        return

    payload = {
        "timestamp": match.group("timestamp"),
        "level": match.group("level"),
        "service": match.group("service"),
        "message": match.group("message"),
    }
    write_payload(payload)
    with stats_lock:
        stats[(branch_name, payload["level"])] += 1

def harvest_from_branch(branch_name, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, port))
    print(f"[{branch_name}] Connected on port {port}")

    buffer = b"" 
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buffer += chunk
            while b"\n" in buffer:
                line_bytes, buffer = buffer.split(b"\n", 1)
                try:
                    line = line_bytes.decode("utf-8").strip()
                except UnicodeDecodeError:
                    continue
                if line:
                    process_line(line, branch_name)
    finally:
        sock.close()

def print_stats_periodically():
    while True:
        time.sleep(3)
        with stats_lock:
            if stats:
                print("\n--- Live Ajio Ingestion Stats ---")
                for (branch, level), count in sorted(stats.items()):
                    print(f"  {branch:20s} {level:10s} {count}")
                print("---------------------------------\n")

if __name__ == "__main__":
    for name, port in BRANCHES:
        t = threading.Thread(target=harvest_from_branch, args=(name, port), daemon=True)
        t.start()

    threading.Thread(target=print_stats_periodically, daemon=True).start()
    print("Ajio Harvester Daemon running. Press Ctrl+C to stop.\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for f in partition_files.values():
            f.close()