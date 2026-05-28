# Import core internal modules using relative imports
# This ensures the package works correctly when installed as a module

from .database import CatalogDatabase  # Handles SQLite metadata storage and file indexing
from .organizer import FileOrganizer    # Core engine responsible for file classification and moving logic