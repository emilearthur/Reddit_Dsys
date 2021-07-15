from typing import Optional
from datetime import datetime
from pydantic import HttpUrl
from pydantic import validator

from app.models.core import IDModelMixin, CoreModel

class SubredditBase(CoreModel):
    """
    Subreddit resources.
    """
    extracted_at: datetime
    name: str
    post_id: str
    title: str
    score: int
    url: HttpUrl
    author: str
    subreddit: str
    description: str
    created_at: datetime
    isscore: bool = False

    @validator("extracted_at", "created_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        """Validate both extracted date and created_at."""
        return value or datetime.now()


class SubredditCreate(SubredditBase):
    """
    Send subreddit post into db.
    """
    pass

class SubredditInDB(IDModelMixin, SubredditCreate):
    """Subreddit in DB."""
    pass