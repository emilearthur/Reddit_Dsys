from fastapi import APIRouter

from app.api.routes.subreddits import router as subreddits_router

router = APIRouter()

router.include_router(subreddits_router, prefix="/subreddit", tags=["subreddit"])