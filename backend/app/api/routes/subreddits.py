from typing import List
from fastapi import APIRouter, Depends, status, Body
from app.api.dependencies.database import get_repository

from app.models.subreddit import SubredditCreate, SubredditInDB
from app.db.repositories.subreddits import SubredditRepository

from app.api.dependencies.subreddits import get_subbreddit_by_name_from_path


router = APIRouter()

@router.post("/", response_model=SubredditInDB, name="subreddit:post-subreddit", status_code=status.HTTP_201_CREATED)
async def create_subredddit(new_subreddit: SubredditCreate = Body(..., embed=True),
                            subreddits_repo: SubredditRepository = Depends(get_repository(SubredditRepository))):
    inserted_subreddit = await subreddits_repo.create_subreddit(new_subreddit=new_subreddit)
    return SubredditInDB(**inserted_subreddit.dict())


@router.get("/", response_model=List[SubredditInDB], name="subreddits:get-subreddit")
async def get_all_subreddit(subreddits_repo: SubredditRepository = Depends(get_repository(SubredditRepository)),
                            ) -> List[SubredditInDB]:
    return await  subreddits_repo.get_all_subreddits()


@router.get("/{name}/", response_model=SubredditInDB, name="subreddit:get-subreddit-by-id")
async def get_todo_by_id(subreddit: SubredditInDB = Depends(get_subbreddit_by_name_from_path)) -> SubredditInDB:
    """Get Method to get subreddit by id."""
    return subreddit