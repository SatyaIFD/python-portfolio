import time
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.utils.logger import get_logger
from app.core.database import CatalogDatabase
from app.core.organizer import FileOrganizer

# Logger for daemon runtime and filesystem events
logger = get_logger(__name__)


class WatchdogHandler(FileSystemEventHandler):
    """
    Bridges OS-level filesystem events to the FileOrganizer logic.

    Converts raw file system signals (create/modify events)
    into structured processing workflows.
    """

    def __init__(self, organizer: FileOrganizer):
        self.organizer = organizer

    def on_created(self, event):
        """
        Triggered when a new file is created in monitored directory.
        """
        if not event.is_directory:
            logger.info(
                f"Watchdog interception: Creation event caught at -> {event.src_path}"
            )
            self.organizer.process_file(Path(event.src_path))

    def on_modified(self, event):
        """
        Triggered when an existing file is modified.

        Useful for detecting downloads that are still being written.
        """
        if not event.is_directory:
            self.organizer.process_file(Path(event.src_path))


def main():
    """
    Entry point for the File Organizer Daemon.

    Responsibilities:
    - Initialize monitoring directory
    - Load database + organizer services
    - Process backlog files
    - Start watchdog observer loop
    """

    logger.info("Initializing File Organizer & Meta-Tagger Daemon Process...")

    # Directory being monitored for incoming files
    watch_target = Path("./sandbox_monitor")

    # Ensure directory exists before starting observer
    watch_target.mkdir(exist_ok=True)

    # Initialize persistence layer (SQLite catalog)
    db = CatalogDatabase(db_path="file_catalog.db")

    # Initialize core file processing engine
    organizer = FileOrganizer(
        target_directory=watch_target,
        db_client=db
    )

    # ----------------------------------------------------------
    # Backlog recovery step:
    # Process any files that already exist before daemon starts
    # ----------------------------------------------------------
    logger.info(
        "Scanning for existing items needing sorting prior to daemon spin-up..."
    )

    for item in watch_target.iterdir():
        if item.is_file():
            organizer.process_file(item)

    # ----------------------------------------------------------
    # Watchdog setup:
    # Listens for real-time filesystem changes
    # ----------------------------------------------------------
    event_handler = WatchdogHandler(organizer)
    observer = Observer()

    observer.schedule(
        event_handler,
        path=str(watch_target),
        recursive=False
    )

    observer.start()

    logger.info(
        f"Daemon fully listening for real-time adjustments inside: "
        f"'{watch_target.resolve()}'"
    )
    logger.info("Press Ctrl+C to stop the background worker process safely.")

    try:
        # Keep main thread alive while observer runs in background
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # Graceful shutdown trigger
        logger.info(
            "Interruption sequence triggered. Stopping background threads gracefully..."
        )
        observer.stop()

    # Ensure observer thread is properly joined before exit
    observer.join()

    logger.info("Daemon cleanly terminated.")


if __name__ == "__main__":
    main()