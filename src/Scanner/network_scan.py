import socket
from datetime import datetime

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
PORTS = [22, 80, 443]

def now():
    return datetime.utcnow().isoformat() + "Z"

def scan_port(host, port):
    sock = socket.socket()
    sock.settimeout(0.3)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def network_scan(host):
    if host not in ALLOWED_HOSTS:
        return {"error": "Niedozwolony host"}

    open_ports = []
    for p in PORTS:
        if scan_port(host, p):
            open_ports.append(p)

    return {
        "timestamp": now(),
        "host": host,
        "open_ports": open_ports
    }
