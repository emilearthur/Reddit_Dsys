"""Function to handle in and out of database."""

from typing import List

from fastapi.param_functions import Query

from app.db.repositories.base import BaseRepository
from app.models.subreddit import SubredditCreate, SubredditInDB


CREATE_SUBREDDIT_QUERY = """
    INSERT INTO posts (extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at)
    VALUES(:extracted_at, :name, :post_id, :title, :score, :url, :author, :subreddit, :description, :created_at)
    RETURNING id, extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at;
"""

GET_ALL_SUBREDDIT_QUERY = """
    SELECT id, extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at
    FROM posts;
"""

GET_SUBREDDIT_BY_NAME_QUERY = """
    SELECT id, extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at
    FROM posts
    WHERE name = :name;
"""

GET_SUBREDDIT_BY_ID_QUERY = """
    SELECT id, extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at
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
        query_values = new_subreddit.dict()
        subreddit = await self.db.fetch_one(query=CREATE_SUBREDDIT_QUERY, values=query_values)
        return SubredditInDB(**subreddit)

    async def get_all_subreddits(self) -> List[SubredditInDB]:
        """Get all subreddits"""
        subreddits = await self.db.fetch_all(query=GET_ALL_SUBREDDIT_QUERY)
        return [SubredditInDB(**subreddit) for subreddit in subreddits]

    async def get_subreddit_by_name(self, *, name:str) -> SubredditInDB:
        subreddit = await self.db.fetch_one(query=GET_SUBREDDIT_BY_NAME_QUERY, values={"name": name})
        if subreddit:
            print(subreddit, name)
            return SubredditInDB(**subreddit)