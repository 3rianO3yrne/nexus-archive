from typing import Annotated

from fastapi import Depends
from sqlmodel import Field, SQLModel, create_engine, Session


class Episode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    series_id: int = Field(default=None, foreign_key="series.id")
    series: int
    season: int
    episode: int
    title: str
    description: str


class Series(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str
    name: str


# TODO: update these to env variables
engine = create_engine(
    "postgresql+psycopg2://postgres:mysecretpassword@db:5432/postgres",
    echo=True,
)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


class DB:
    def init_db():
        SQLModel.metadata.create_all(engine)
