import tkinter as tk
from tkinter import filedialog, messagebox

import requests


# ===================================================================
# Search Engine GUI
# ===================================================================
#
# This Tkinter-based desktop interface provides a simple
# administration panel for the Local Document Search API.
#
# Features:
# - Select local directories visually
# - Trigger indexing via FastAPI backend
# - Display indexing success/failure messages
# - Lightweight and easy to run
#
# Workflow:
# 1. User selects a folder
# 2. GUI sends POST request to FastAPI backend
# 3. Backend indexes documents
# 4. GUI displays indexing results
#
# ===================================================================


class SearchEngineGUI:
    """
    Desktop GUI client for managing document indexing.

    This interface acts as a frontend controller for the
    FastAPI search backend.
    """

    def __init__(self, root):
        """
        Initialize the GUI window and components.

        Args:
            root:
                Tkinter root window instance
        """

        self.root = root

        # -----------------------------------------------------------
        # Main Window Configuration
        # -----------------------------------------------------------
        self.root.title("Local Doc Search API Admin")

        # Window size: Width x Height
        self.root.geometry("450x200")

        # -----------------------------------------------------------
        # Instruction Label
        # -----------------------------------------------------------
        #
        # Provides guidance to the user
        #
        self.label = tk.Label(
            root,
            text=(
                "Select a local folder to index "
                "into the API backend:"
            )
        )

        self.label.pack(pady=15)

        # -----------------------------------------------------------
        # Directory Selection Button
        # -----------------------------------------------------------
        #
        # Clicking this button opens a folder picker dialog
        #
        self.btn_select = tk.Button(
            root,
            text="Browse & Index Directory",

            # Action callback
            command=self.select_and_index,

            # Styling
            bg="#2196F3",
            fg="white"
        )

        self.btn_select.pack(pady=10)

        # -----------------------------------------------------------
        # Backend Status Label
        # -----------------------------------------------------------
        #
        # Displays current API target server
        #
        self.status_label = tk.Label(
            root,
            text="API Backend Target: http://127.0.0.1:8000",
            fg="grey"
        )

        self.status_label.pack(
            side="bottom",
            pady=10
        )

    def select_and_index(self):
        """
        Open directory picker and trigger indexing request.

        Steps:
        1. Open folder selection dialog
        2. Send POST request to FastAPI backend
        3. Display success or error popup
        """

        # -----------------------------------------------------------
        # Open native folder selection dialog
        # -----------------------------------------------------------
        folder_selected = filedialog.askdirectory()

        # Continue only if a folder was selected
        if folder_selected:

            try:
                # ---------------------------------------------------
                # FastAPI indexing endpoint
                # ---------------------------------------------------
                url = "http://127.0.0.1:8000/api/v1/index"

                # ---------------------------------------------------
                # Send indexing request to backend
                # ---------------------------------------------------
                response = requests.post(
                    url,

                    # JSON request body
                    json={
                        "directory_path": folder_selected
                    },

                    # Prevent hanging requests
                    timeout=15
                )

                # ---------------------------------------------------
                # Successful indexing response
                # ---------------------------------------------------
                if response.status_code == 200:

                    # Parse API response JSON
                    data = response.json()

                    messagebox.showinfo(
                        "Success",

                        (
                            f"Done! Indexed "
                            f"{data['documents_indexed']} "
                            f"documents successfully."
                        )
                    )

                # ---------------------------------------------------
                # Backend returned an error
                # ---------------------------------------------------
                else:
                    messagebox.showerror(
                        "Backend Error",

                        (
                            "Server responded with error:\n\n"
                            f"{response.text}"
                        )
                    )

            except Exception as e:
                # ---------------------------------------------------
                # Handle connection failures
                # ---------------------------------------------------
                #
                # Example:
                # - Backend server not running
                # - Network issue
                # - Timeout
                #
                messagebox.showerror(
                    "Connection Error",

                    (
                        "Could not connect to FastAPI server.\n"
                        "Is it running?\n\n"
                        f"Error: {e}"
                    )
                )


# ===================================================================
# Application Entry Point
# ===================================================================
#
# This block runs only when the script is executed directly.
#
# Example:
#     python gui.py
#
# ===================================================================

if __name__ == "__main__":

    # Create main Tkinter window
    root = tk.Tk()

    # Initialize GUI application
    app = SearchEngineGUI(root)

    # Start GUI event loop
    root.mainloop()