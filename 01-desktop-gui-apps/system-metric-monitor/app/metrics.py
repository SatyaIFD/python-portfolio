import psutil
import time
import subprocess
import platform

def get_system_metrics():
    """Fetches real-time CPU, RAM, Disk, and Network Ping telemetry."""
    # CPU usage percentage evaluated over a tight 0.1-second polling window
    cpu_usage = psutil.cpu_percent(interval=0.1)
    
    # RAM consumption metrics
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    
    # Storage readouts for the primary root path
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    
    # Network latency detection
    ping_time = -1
    try:
        # Check system OS to apply correct ping flags
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-W', '1', '8.8.8.8']
        
        start_time = time.time()
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if result.returncode == 0:
            ping_time = int((time.time() - start_time) * 1000)
    except Exception:
        ping_time = -1  # Indicates network unreachable or timeout
        
    return {
        "cpu": cpu_usage,
        "ram": ram_usage,
        "disk": disk_usage,
        "ping": ping_time
    }