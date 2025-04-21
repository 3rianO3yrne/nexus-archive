from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..models import Episode, SessionDep, Topic

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/episode/")
def get_all_episode(session: SessionDep):
    statement = select(Episode)
    results = session.exec(statement).all()
    # statement = select(Episode, Topic).join(Topic, isouter=True)
    # results = session.exec(statement)
    # for episode, topic in results:
    #     result =
    return results


@router.get("/episode/{episode_id}")
async def get_episode(episode_id: int, session: SessionDep) -> Episode:
    episode = session.get(Episode, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode


@router.post("/episode/")
def create_episode(episode: Episode, session: SessionDep) -> Episode:
    session.add(episode)
    session.commit()
    session.refresh(episode)
    return episode


@router.patch("/episodes/{episode_id}", response_model=Episode)
def update_episode(episode_id: int, episode: Episode, session: SessionDep):
    episode_db = session.get(Episode, episode_id)
    if not episode_db:
        raise HTTPException(status_code=404, detail="Episode not found")
    series_data = episode.model_dump(exclude_unset=True)
    episode_db.sqlmodel_update(series_data)
    session.add(episode_db)
    session.commit()
    session.refresh(episode_db)
    return episode_db
