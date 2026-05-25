from PySide6.QtWidgets import (QMainWindow, QTableView, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLabel, QPushButton, QFileDialog)
from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtGui import QColor
import os

# Import your custom engine
from .metrics import DataProcessor

class DataTableModel(QAbstractTableModel):
    def __init__(self, data, anomaly_map=None):
        super().__init__()
        self._data = data
        # anomaly_map format: {"ColumnName": [row_indices]}
        self.anomaly_map = anomaly_map or {}

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        row = index.row()
        col = index.column()
        col_name = self._data.columns[col]

        # 1. Handle Text Display
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[row, col])

        # 2. Handle Visual Highlighting of Anomalies
        if role == Qt.ItemDataRole.BackgroundRole:
            if col_name in self.anomaly_map and row in self.anomaly_map[col_name]:
                return QColor(255, 204, 204)  # Light Red for errors
        
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        return None


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataShield | Validator & Cleaner")
        self.resize(1000, 700)
        self.setAcceptDrops(True)

        self.processor = None

        # Main Layout
        self.central = QWidget()
        self.layout = QVBoxLayout(self.central)

        # Top Header
        self.label = QLabel("Drag & Drop CSV/JSON to analyze")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; color: #555;")
        
        # Table View
        self.table = QTableView()
        self.table.setAlternatingRowColors(True)
        
        # Action Bar (Bottom)
        self.action_layout = QHBoxLayout()
        self.btn_validate = QPushButton("Run Validation (Auto)")
        self.btn_export = QPushButton("Clean & Export CSV")
        self.btn_export.setEnabled(False)
        self.btn_export.clicked.connect(self.export_file)
        
        self.action_layout.addWidget(self.btn_validate)
        self.action_layout.addWidget(self.btn_export)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.action_layout)

        self.setCentralWidget(self.central)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = event.mimeData().urls()
        if not files: return

        file_path = files[0].toLocalFile()
        if os.path.exists(file_path) and file_path.lower().endswith((".csv", ".json")):
            self.load_file(file_path)
        else:
            self.label.setText("❌ Invalid file. Please drop a CSV or JSON.")

    def load_file(self, path):
        try:
            # Initialize Processor
            self.processor = DataProcessor(path)
            
            # Example: Auto-run some basic validation rules
            # In a real app, you'd let the user pick these from a menu
            rules = {}
            for col in self.processor.df.columns:
                if "email" in col.lower(): rules[col] = "Email"
                # Add more auto-detection logic here
            
            # Run validation
            anomalies = self.processor.validate_all(rules)
            
            # Update Table
            model = DataTableModel(self.processor.df, anomalies)
            self.table.setModel(model)
            
            # Update UI state
            self.label.setText(f"File: {os.path.basename(path)} | Status: {self.processor.get_health_report()['total_anomalies']} errors found.")
            self.btn_export.setEnabled(True)

        except Exception as e:
            self.label.setText(f"❌ Error: {str(e)}")

    def export_file(self):
        if not self.processor: return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Cleaned Data", "", "CSV Files (*.csv)")
        if save_path:
            dropped_count = self.processor.clean_and_export(save_path)
            self.label.setText(f"✅ Saved! Removed {dropped_count} anomalous rows.")
            # Refresh table to show clean data
            self.table.setModel(DataTableModel(self.processor.df))