"""Function to handle in and out of database."""

from typing import List

from fastapi import status, HTTPException

from app.db.repositories.base import BaseRepository
from app.models.subreddit import SubredditCreate, SubredditInDB, SubredditIntoDB

from utils.datetime_fixer import datetimefixer


CREATE_SUBREDDIT_QUERY = """
    INSERT INTO posts (extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at, isscore)
    VALUES(:extracted_at, :name, :post_id, :title, :score, :url, :author, :subreddit, :description, :created_at, :isscore);
"""

GET_ALL_SUBREDDIT_QUERY = """
    SELECT id, extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at, isscore
    FROM posts;
"""

GET_SUBREDDIT_BY_NAME_QUERY = """
    SELECT id, extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at, isscore
    FROM posts
    WHERE name = :name;
"""

GET_SUBREDDIT_BY_POST_ID_QUERY = """
    SELECT id, extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at, isscore
    FROM posts
    WHERE post_id = :post_id;
"""

GET_SUBREDDIT_BY_ID_QUERY = """
    SELECT id, extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at, isscore
    FROM posts
    WHERE id = :id;
"""

UPDATE_SUBREDDIT_AFTER_SCORING_QUERY = """
    UPDATE posts
    SET isscore = 'true'
    WHERE id = :id;
"""

class SubredditRepository(BaseRepository):
    """
    All database actions assocated with Subreddit resources.
    """

    async def create_subreddit(self, *, new_subreddit: SubredditCreate) -> SubredditInDB:
        """Input scrapped subreddit into db."""
        if await self.get_subreddit_by_post_id(post_id=new_subreddit.post_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"subreddit with id {new_subreddit.post_id} already in db.")
        params = SubredditIntoDB(**new_subreddit.dict(exclude={"extracted_at", "created_at"}))
        datetime_fixed  = datetimefixer(extracted_at=new_subreddit.extracted_at, created_at=new_subreddit.created_at)
        updated_params = params.copy(update=datetime_fixed.dict())
        subreddit = await self.db.fetch_one(query=CREATE_SUBREDDIT_QUERY, values=updated_params.dict())
        return SubredditInDB(**subreddit)

    async def get_all_subreddits(self) -> List[SubredditInDB]:
        """Get all subreddits"""
        subreddits = await self.db.fetch_all(query=GET_ALL_SUBREDDIT_QUERY)
        return [SubredditInDB(**subreddit) for subreddit in subreddits]

    async def get_subreddit_by_name(self, *, name:str) -> SubredditInDB:
        subreddit = await self.db.fetch_one(query=GET_SUBREDDIT_BY_NAME_QUERY, values={"name": name})
        if subreddit:
            return SubredditInDB(**subreddit)

    async def get_subreddit_by_post_id(self, *, post_id: str) -> SubredditInDB:
        subreddit = await self.db.fetch_one(query=GET_SUBREDDIT_BY_POST_ID_QUERY, values={"post_id": post_id})
        if subreddit:
            return SubredditInDB(**subreddit)