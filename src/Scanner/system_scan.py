import platform
import socket
import psutil
from datetime import datetime

def now():
    return datetime.utcnow().isoformat() + "Z"

def system_scan():
    return {
        "timestamp": now(),
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "kernel": platform.release(),
        "cpu_usage": psutil.cpu_percent(1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
    }
