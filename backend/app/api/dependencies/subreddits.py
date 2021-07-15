"""Dependies for subreddits."""

from app.api.dependencies.database import get_repository
from app.db.repositories.subreddits import SubredditRepository
from fastapi import Depends, HTTPException, Path, status
from app.models.subreddit import SubredditInDB



async def get_subbreddit_by_id_from_path(subreddit_id: int = Path(..., ge=1),
                                         subreddits_repo: SubredditRepository = Depends(get_repository(SubredditRepository))
                                         ) -> SubredditInDB:
    """Dependency to get subreddit using id."""
    subreddit = await subreddits_repo.get_subreddit_by_id(id=subreddit_id)
    if not subreddit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subreddit with id not found.")
    return subreddit


async def get_subbreddit_by_name_from_path(name: str = Path(..., min_length=3, regex="^[a-zA-Z0-9_-]+$"),
                                         subreddits_repo: SubredditRepository = Depends(get_repository(SubredditRepository))
                                         ) -> SubredditInDB:
    """Dependency to get subreddit using name."""
    subreddit = await subreddits_repo.get_subreddit_by_name(name=name)
    if not subreddit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subreddit name not found.")
    return subreddit