from PySide6.QtWidgets import QMainWindow, QTableView, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QAbstractTableModel
import os


class DataTableModel(QAbstractTableModel):
    """
    Bridge between Pandas DataFrame and Qt Table View.
    """

    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None


class MainUI(QMainWindow):
    """
    Main UI for Data Validator & Cleaner.
    Supports drag-and-drop CSV/JSON loading.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Validator & Cleaner")

        # Enable drag & drop
        self.setAcceptDrops(True)

        self.central = QWidget()
        self.layout = QVBoxLayout(self.central)

        self.label = QLabel("Drag CSV/JSON file here to start")
        self.table = QTableView()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)

        self.setCentralWidget(self.central)

    # -----------------------------
    # DRAG ENTER EVENT
    # -----------------------------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    # -----------------------------
    # DROP EVENT
    # -----------------------------
    def dropEvent(self, event):
        files = event.mimeData().urls()

        # Edge case: no file dropped
        if not files:
            self.label.setText("❌ No file detected")
            return

        # Only take first file
        file_path = files[0].toLocalFile()

        # Edge case: invalid path
        if not os.path.exists(file_path):
            self.label.setText("❌ File does not exist")
            return

        # Validate file type
        if not (file_path.endswith(".csv") or file_path.endswith(".json")):
            self.label.setText("❌ Only CSV or JSON allowed")
            return

        # Success case
        self.label.setText(f"Loaded: {os.path.basename(file_path)}")

        print("File dropped:", file_path)

        # NEXT STEP: load file into table
        self.load_file(file_path)

    # -----------------------------
    # FILE LOADER (needed next)
    # -----------------------------
    def load_file(self, path):
        import pandas as pd

        try:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            else:
                df = pd.read_json(path)

            model = DataTableModel(df)
            self.table.setModel(model)

        except Exception as e:
            self.label.setText(f"❌ Error loading file: {str(e)}")