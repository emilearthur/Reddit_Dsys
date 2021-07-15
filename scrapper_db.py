from datetime import datetime
from pydantic import BaseModel, validator
from pydantic import HttpUrl
from datetime import datetime


class RedditData(BaseModel):
    extracted_at: datetime
    id: str
    score: int
    title: str
    url: HttpUrl
    author: str
    subreddit: str
    description: str
    created_at: datetime

    @validator("extracted_at", "created_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        """Validate both extracted date and created_at."""
        return value or datetime.now()