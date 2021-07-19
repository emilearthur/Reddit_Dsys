from typing import Optional
from datetime import datetime
from pydantic import HttpUrl
from pydantic import validator

from app.models.core import IDModelMixin, CoreModel

class SubredditBase(CoreModel):
    """
    Subreddit resources.
    """
    name: str
    post_id: str
    title: str
    score: int
    url: HttpUrl
    author: str
    subreddit: str
    description: str
    isscore: bool = False


class SubredditCreate(SubredditBase):
    """
    Send subreddit post into db.
    """
    extracted_at: float
    created_at: float

class SubredditIntoDB(SubredditBase):
    """
    extracted_at and converted at in datetime instead of float
    """
    extracted_at: Optional[datetime]
    created_at: Optional[datetime]
    
    @validator("extracted_at", "created_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        """Validate both extracted date and created_at."""
        return value or datetime.now()

class SubredditInDB(IDModelMixin, SubredditIntoDB):
    """Subreddit in DB."""
    pass


class Extracted_Created_Date(CoreModel):
    """Fixes timezone offset."""
    extracted_at: datetime
    created_at: datetime