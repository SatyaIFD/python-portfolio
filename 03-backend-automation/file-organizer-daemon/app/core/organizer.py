import time
from pathlib import Path
from app.utils.logger import get_logger
from app.core.database import CatalogDatabase

logger = get_logger(__name__)

class FileOrganizer:
    """Encapsulates the sorting routing rules, structural renaming, and indexing actions."""
    
    CATEGORY_MAPPING = {
        'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.csv', '.pptx'],
        'Media': ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mp3', '.mov', '.wav'],
        'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
        'Executables': ['.exe', '.dmg', '.pkg', '.sh', '.msi']
    }

    def __init__(self, target_directory: Path, db_client: CatalogDatabase):
        self.target_directory = Path(target_directory)
        self.db = db_client

    def determine_category(self, extension: str) -> str:
        """Determines the operational folder category based on file suffix mapping."""
        ext_lower = extension.lower()
        for category, extensions in self.CATEGORY_MAPPING.items():
            if ext_lower in extensions:
                return category
        return 'Other'

    def process_file(self, file_path: Path) -> None:
        """Applies sorting logic, moves the file safely, and writes metadata to the DB."""
        file_path = Path(file_path)
        
        # Guard clause: ensure file exists and isn't a directory/hidden file
        if not file_path.exists() or file_path.is_dir() or file_path.name.startswith('.'):
            return

        # Settle active writes or lock conditions before processing
        time.sleep(0.5)

        original_name = file_path.name
        extension = file_path.suffix
        category = self.determine_category(extension)
        
        # Establish targeted destination directory configuration
        destination_dir = self.target_directory / category
        destination_dir.mkdir(parents=True, exist_ok=True)
        
        # Standardized file naming formatting template: [Lower_Case_Filename_Spaced]
        clean_name = file_path.stem.strip().replace(" ", "_").lower()
        destination_path = destination_dir / f"{clean_name}{extension}"

        # Deconflict file collisions safely
        counter = 1
        while destination_path.exists():
            destination_path = destination_dir / f"{clean_name}_{counter}{extension}"
            counter += 1

        try:
            file_size = file_path.stat().st_size
            file_path.rename(destination_path)
            logger.info(f"Successfully relocated: '{original_name}' -> '{destination_path.relative_to(self.target_directory)}'")
            
            # Catalog finalized telemetry attributes into DB layer
            self.db.catalog_file(
                original_name=original_name,
                current_path=destination_path,
                extension=extension,
                size=file_size,
                category=category
            )
        except Exception as e:
            logger.error(f"Error handling process workflow lifecycle on file {original_name}: {str(e)}")