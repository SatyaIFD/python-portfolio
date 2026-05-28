import pytest
from pathlib import Path
import sqlite3

from app.core.database import CatalogDatabase
from app.core.organizer import FileOrganizer


@pytest.fixture
def temp_workspace(tmp_path):
    """
    Creates an isolated temporary filesystem workspace.

    Used to simulate real file system operations without touching
    the actual user environment.
    """
    watch_dir = tmp_path / "watch_folder"
    watch_dir.mkdir()
    return watch_dir


@pytest.fixture
def mock_db(tmp_path):
    """
    Creates a temporary SQLite database instance.

    Ensures tests run in isolation with no shared state.
    """
    db_file = tmp_path / "test_catalog.db"
    return CatalogDatabase(db_path=str(db_file))


def test_determine_category():
    """
    Validates extension-to-category mapping logic.
    Ensures FileOrganizer correctly classifies file types.
    """

    organizer = FileOrganizer(
        target_directory=Path("."),
        db_client=None
    )

    assert organizer.determine_category(".pdf") == "Documents"
    assert organizer.determine_category(".png") == "Media"
    assert organizer.determine_category(".xyz") == "Other"


def test_file_sorting_and_indexing(temp_workspace, mock_db):
    """
    End-to-end test:
    - Creates a file
    - Runs organizer logic
    - Verifies file relocation
    - Verifies database indexing
    """

    organizer = FileOrganizer(
        target_directory=temp_workspace,
        db_client=mock_db
    )

    # -----------------------------
    # Arrange: Create sample file
    # -----------------------------
    raw_file = temp_workspace / "User Manual Notes.txt"
    raw_file.write_text("Sample arbitrary contents tracking data parameters.")

    # -----------------------------
    # Act: Process the file
    # -----------------------------
    organizer.process_file(raw_file)

    # -----------------------------
    # Assert: File moved correctly
    # -----------------------------
    expected_destination = (
        temp_workspace / "Documents" / "user_manual_notes.txt"
    )

    assert expected_destination.exists()
    assert not raw_file.exists()

    # -----------------------------
    # Assert: Database entry exists
    # -----------------------------
    with sqlite3.connect(mock_db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT original_name, current_path, detected_category
            FROM file_catalog
        """)
        record = cursor.fetchone()

    assert record is not None
    assert record[0] == "User Manual Notes.txt"
    assert record[1] == str(expected_destination)
    assert record[2] == "Documents"