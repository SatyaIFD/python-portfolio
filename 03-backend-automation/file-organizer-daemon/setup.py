from setuptools import setup, find_packages

setup(
    # Name of your Python package (used when publishing or installing)
    name="file_organizer_daemon",

    # Current version of the package (follow semantic versioning)
    version="1.0.0",

    # Automatically discover all packages inside the project directory
    packages=find_packages(),

    # External dependencies required for this project to run
    install_requires=[
        # watchdog is used to monitor file system events (create, modify, delete, etc.)
        "watchdog==4.0.0",
    ],

    # Defines command-line scripts that will be installed with the package
    entry_points={
        "console_scripts": [
            # This creates a terminal command: run-daemon
            # It maps to the main() function inside app/core/daemon.py
            "run-daemon=app.core.daemon:main",
        ],
    },
)