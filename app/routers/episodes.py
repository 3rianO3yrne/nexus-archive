from fastapi import APIRouter, Depends, HTTPException
from ..models import Episode

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


# @router.get("/episodes/{episodes}")
# async def read_episodes(episodes | none):
#     episodes
#     return {"Hello": "World"}


@router.get("/episode/{episode_id}")
async def read_item(episode_id):
    return {"episode_id": episode_id}


@router.post("episodes")
def post_item(episode: Episode):
    return Episode
