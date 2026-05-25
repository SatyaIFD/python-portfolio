import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.ui import MainUI

def main():
    """
    Entry point of the DataShield: Validator & Cleaner application.
    """
    
    # 1. High DPI Support (Crucial for modern monitors)
    # This ensures text and buttons aren't tiny or blurry on 4K screens.
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)

    # 2. Modern Styling
    app.setStyle("Fusion")

    # 3. Application Metadata
    app.setApplicationName("DataShield")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("YourProject")

    # 4. Optional: Set Window Icon
    # icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
    # if os.path.exists(icon_path):
    #     app.setWindowIcon(QIcon(icon_path))

    # 5. Initialize & Show Window
    window = MainUI()
    
    # Optional: Start centered on screen
    screen_geometry = app.primaryScreen().availableGeometry()
    window.resize(1100, 750)  # Slightly larger default for data views
    window.move(
        (screen_geometry.width() - window.width()) // 2,
        (screen_geometry.height() - window.height()) // 2
    )
    
    window.show()

    # 6. Clean Exit
    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing application...")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()