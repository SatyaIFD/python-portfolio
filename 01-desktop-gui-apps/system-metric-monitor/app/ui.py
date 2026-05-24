import customtkinter as ctk
import threading
import time
from app.metrics import get_system_metrics
from app.database import initialize_database, log_spike

class MetricMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize internal log structures
        initialize_database()
        
        # Master Window Setup
        self.title("Pulse Monitor Dashboard")
        self.geometry("450x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        
        # Thread lifecycle tracking state
        self.is_running = True
        
        # Spin up detached worker thread for background data polling
        self.worker_thread = threading.Thread(target=self.metrics_polling_engine, daemon=True)
        self.worker_thread.start()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close_handler)

    def setup_ui(self):
        """Constructs core interface visual architecture."""
        self.header = ctk.CTkLabel(self, text="⚡ SYSTEM TELEMETRY", font=("Helvetica", 18, "bold"))
        self.header.pack(pady=20)
        
        # CPU UI Components
        self.cpu_lbl = ctk.CTkLabel(self, text="CPU Utilization: 0.0%", font=("Helvetica", 13))
        self.cpu_lbl.pack(pady=(5, 2))
        self.cpu_bar = ctk.CTkProgressBar(self, width=320)
        self.cpu_bar.set(0)
        self.cpu_bar.pack(pady=5)
        
        # RAM UI Components
        self.ram_lbl = ctk.CTkLabel(self, text="Memory Commitment: 0.0%", font=("Helvetica", 13))
        self.ram_lbl.pack(pady=(15, 2))
        self.ram_bar = ctk.CTkProgressBar(self, width=320)
        self.ram_bar.set(0)
        self.ram_bar.pack(pady=5)
        
        # Network Latency UI Components
        self.ping_lbl = ctk.CTkLabel(self, text="ICMP Network Ping: Connecting...", font=("Helvetica", 13))
        self.ping_lbl.pack(pady=25)

    def metrics_polling_engine(self):
        """Asynchronous collection runtime. Evaluates thresholds and triggers loggers."""
        while self.is_running:
            data = get_system_metrics()
            
            # Evaluate telemetry for anomaly spikes (>80% Warning, >95% Critical)
            for key in ['cpu', 'ram']:
                if data[key] >= 95.0:
                    log_spike(key.upper(), data[key], "CRITICAL")
                elif data[key] >= 80.0:
                    log_spike(key.upper(), data[key], "WARNING")
            
            # Pass hardware metric structures back into the main rendering thread
            self.after(0, self.refresh_ui_elements, data)
            time.sleep(1.0)

    def refresh_ui_elements(self, data):
        """Updates UI display with the fresh hardware snapshot."""
        self.cpu_lbl.configure(text=f"CPU Utilization: {data['cpu']}%")
        self.cpu_bar.set(data['cpu'] / 100.0)
        
        self.ram_lbl.configure(text=f"Memory Commitment: {data['ram']}%")
        self.ram_bar.set(data['ram'] / 100.0)
        
        if data['ping'] != -1:
            self.ping_lbl.configure(text=f"ICMP Network Ping: {data['ping']} ms", text_color=["#107c41", "#107c41"])
        else:
            self.ping_lbl.configure(text="ICMP Network Ping: TIMEOUT / OFFLINE", text_color="#a80000")

    def on_close_handler(self):
        """Clean shutdown execution sequence."""
        self.is_running = False
        self.destroy()