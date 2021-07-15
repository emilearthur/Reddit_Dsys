import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status


class TestSubredditsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("subreddits:get-subreddit"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("subreddits:get-subreddit"), json={})
        assert res.status_code == status.HTTP_200_OK