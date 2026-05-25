import sys
from PySide6.QtWidgets import QApplication
from app.ui import MainUI


if __name__ == "__main__":
    """
    Entry point of the application.

    This script initializes the Qt application, applies a modern UI style,
    launches the main window, and starts the event loop.
    """

    # Create the Qt application instance
    app = QApplication(sys.argv)

    # Apply a modern, cross-platform UI style
    app.setStyle("Fusion")

    # Create main application window
    window = MainUI()

    # Set initial window size
    window.resize(900, 600)

    # Display the window
    window.show()

    # Start Qt event loop and exit cleanly when closed
    sys.exit(app.exec())