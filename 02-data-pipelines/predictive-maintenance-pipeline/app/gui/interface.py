import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from app.core.data_processor import DataProcessor
from app.core.model import MaintenanceModel

class MaintenanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Predictive Maintenance Monitor Console")
        self.geometry("680x480")
        
        self.processor = DataProcessor(window_size=5)
        self.model_manager = MaintenanceModel()
        self.data = None

        self._build_ui()

    def _build_ui(self):
        # Header layout frame
        header_frame = ttk.Frame(self, padding=10)
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame, 
            text="Industrial Equipment Health Pipeline", 
            font=("Arial", 14, "bold")
        )
        title_label.pack(side=tk.LEFT)

        # Main Workspace tab controls
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.control_tab = ttk.Frame(self.notebook)
        self.data_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.control_tab, text="Pipeline Administration")
        self.notebook.add(self.data_tab, text="Live Telemetry View")

        self._setup_control_tab()
        self._setup_data_tab()

    def _setup_control_tab(self):
        layout = ttk.Frame(self.control_tab, padding=20)
        layout.pack(fill=tk.BOTH, expand=True)

        btn_generate = ttk.Button(layout, text="1. Ingest Data & Extract Features", command=self.handle_ingestion)
        btn_generate.pack(fill=tk.X, pady=10)

        btn_train = ttk.Button(layout, text="2. Train & Evaluate Classifier", command=self.handle_training)
        btn_train.pack(fill=tk.X, pady=10)

        self.status_text = tk.Text(layout, height=12, wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def _setup_data_tab(self):
        self.tree = ttk.Treeview(self.data_tab, columns=("ts", "temp", "vib", "anomaly"), show="headings")
        self.tree.heading("ts", text="Timestamp")
        self.tree.heading("temp", text="Temperature (°C)")
        self.tree.heading("vib", text="Vibration (mm/s)")
        self.tree.heading("anomaly", text="Predicted Fault Target")
        
        self.tree.pack(fill=tk.BOTH, expand=True)

    def append_log(self, text: str):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, text + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def handle_ingestion(self):
        raw_df = self.processor.generate_synthetic_data(n_samples=500)
        self.data = self.processor.extract_features(raw_df)
        self.append_log(f"[SUCCESS] Ingested raw metrics. Features shape matching: {self.data.shape}")
        
        # Populate the live monitoring Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for _, row in self.data.head(25).iterrows():
            self.tree.insert("", tk.END, values=(
                row["timestamp"], 
                f"{row['temperature']:.2f}", 
                f"{row['vibration']:.2f}", 
                "CRITICAL SYSTEM FAULT" if row["failure_target"] == 1 else "Normal Operating State"
            ))

    def handle_training(self):
        if self.data is None:
            messagebox.showerror("Pipeline Execution Error", "Ingest and structure industrial telemetry data sets first.")
            return
        
        self.append_log("[PIPELINE RUNNING] Extracting transforms and optimizing tree structures...")
        metrics = self.model_manager.train(self.data)
        self.model_manager.save_artifacts()
        
        accuracy = metrics["report"]["accuracy"]
        self.append_log(f"[METRIC REPORT] Pipeline successfully trained model with Accuracy: {accuracy:.2%}")
        messagebox.showinfo("Pipeline Complete", f"Model trained with accuracy: {accuracy:.2%}")

if __name__ == "__main__":
    app = MaintenanceApp()
    app.mainloop()
