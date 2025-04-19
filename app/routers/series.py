from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..models import Series, SessionDep

router = APIRouter()


@router.get("/series/")
def get_all_series(session: SessionDep) -> list[Series]:
    series = session.exec(select(Series)).all()
    return series


@router.get("/series/{series_id}")
async def get_series(series_id: int, session: SessionDep) -> Series:
    series = session.get(Series, series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return series


@router.post("/series/")
def create_series(series: Series, session: SessionDep) -> Series:
    session.add(series)
    session.commit()
    session.refresh(series)
    return series


@router.patch("/series/{series_id}", response_model=Series)
def update_hero(series_id: int, series: Series, session: SessionDep):
    series_db = session.get(Series, series_id)
    if not series_db:
        raise HTTPException(status_code=404, detail="Series not found")
    series_data = series.model_dump(exclude_unset=True)
    series_db.sqlmodel_update(series_data)
    session.add(series_db)
    session.commit()
    session.refresh(series_db)
    return series_db
