import socket
from datetime import datetime

def now():
    return datetime.utcnow().isoformat() + "Z"

def scan_port(host, port):
    sock = socket.socket()
    sock.settimeout(0.5)
    result = sock.connect_ex((host, port))
    sock.close()
    return port, (result == 0)

def network_scan(host, ports=(22,80,443)):
    report = {
        "timestamp": now(),
        "target": host,
        "open_ports": [],
        "closed_ports": []
    }
    for p in ports:
        port, ok = scan_port(host, p)
        if ok:
            report["open_ports"].append(port)
        else:
            report["closed_ports"].append(port)
    return report