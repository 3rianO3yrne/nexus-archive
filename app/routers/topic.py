from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..models import Topic, SessionDep

router = APIRouter()


@router.get("/topic/")
def get_all_topic(session: SessionDep) -> list[Topic]:
    topic = session.exec(select(Topic)).all()
    return topic


@router.get("/topic/{topic_id}")
async def get_topic(topic_id: int, session: SessionDep) -> Topic:
    topic = session.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.post("/topic/")
def create_topic(topic: Topic, session: SessionDep) -> Topic:
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return topic


@router.patch("/topic/{topic_id}", response_model=Topic)
def update_hero(topic_id: int, topic: Topic, session: SessionDep):
    topic_db = session.get(Topic, topic_id)
    if not topic_db:
        raise HTTPException(status_code=404, detail="Topic not found")
    topic_data = topic.model_dump(exclude_unset=True)
    topic_db.sqlmodel_update(topic_data)
    session.add(topic_db)
    session.commit()
    session.refresh(topic_db)
    return topic_db
