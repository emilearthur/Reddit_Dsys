from pydantic import BaseModel
from pydantic import HttpUrl
from typing import Optional
from datetime import datetime


class Subreddit(BaseModel):
    """
    Subreddit resources.
    """
    extracted_at: float
    name: str
    post_id: str
    title: str
    score: int
    url: str
    author: str
    subreddit: str
    description: str
    created_at: float
    isscore: bool = False


class SubredditDB(Subreddit):
    """
    Subreddit resources.
    """
    url: HttpUrl
    extracted_at: Optional[datetime]
    created_at: Optional[datetime]


class Extracted_Created_Date(BaseModel):
    """Fixes timezone offset."""
    extracted_at: datetime
    created_at: datetime