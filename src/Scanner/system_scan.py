import platform
import socket
import psutil
from datetime import datetime

def now():
    return datetime.utcnow().isoformat() + "Z"

def system_scan():
    data = {
        "timestamp": now(),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "kernel": platform.release(),
        "cpu_percent": psutil.cpu_percent(1),
        "cpu_count": psutil.cpu_count(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
    }
    return data