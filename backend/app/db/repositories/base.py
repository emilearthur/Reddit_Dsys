"""Base Repository."""

from databases import Database



class BaseRepository:
    """Base class."""

    def __init__(self, db: Database) -> None:
        """Initialize. db (Database): Initalize database."""
        self.db = db