import struct
import sys

LEVEL_CODE = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
CODE_LEVEL = {v: k for k, v in LEVEL_CODE.items()}

def read_records(filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    offset = 0
    records = []
    while offset < len(data):
        (record_len,) = struct.unpack_from("!I", data, offset)
        offset += 4

        record_bytes = data[offset : offset + record_len]
        offset += record_len

        ts_bytes, level_byte, service_len = struct.unpack_from("!19sBH", record_bytes, 0)
        pos = 19 + 1 + 2

        service = record_bytes[pos : pos + service_len].decode("utf-8")
        pos += service_len

        (message_len,) = struct.unpack_from("!H", record_bytes, pos)
        pos += 2

        message = record_bytes[pos : pos + message_len].decode("utf-8")

        records.append({
            "timestamp": ts_bytes.decode("ascii").strip(),
            "level": CODE_LEVEL[level_byte],
            "service": service,
            "message": message,
        })
    return records

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ajio_reader.py <path-to-.bin-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    records = read_records(filepath)
    print(f"\nFound {len(records)} records in {filepath}:\n")
    for r in records:
        print(f"{r['timestamp']} | {r['level']} | {r['service']} | {r['message']}")