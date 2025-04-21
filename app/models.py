from typing import Annotated

from fastapi import Depends
from sqlmodel import Field, SQLModel, create_engine, Session, Relationship


class Series(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str
    name: str
    episodes: list["Episode"] = Relationship(back_populates="series")


class EpisodeTopic(SQLModel, table=True):
    episode_id: int | None = Field(
        default=None, foreign_key="episode.id", primary_key=True
    )
    topic_id: int = Field(default=None, foreign_key="topic.id", primary_key=True)


class Episode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    series_id: int = Field(default=None, foreign_key="series.id")
    series: Series = Relationship(back_populates="episodes")
    season: int
    episode: int
    title: str
    description: str | None
    topics: list["Topic"] = Relationship(
        back_populates="episodes", link_model=EpisodeTopic
    )


class Topic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    topic_name: str
    episodes: list["Episode"] = Relationship(
        back_populates="topics", link_model=EpisodeTopic
    )


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

    def seed():
        with Session(engine) as session:
            series_1 = Series(code="TNG", name="Star Trek: The Next Generation")
            series_2 = Series(code="DS9", name="Star Trek: Deep Space 9")
            series_3 = Series(code="TOS", name="Star Trek: The Original Series")
            series_4 = Series(code="VOY", name="Star Trek: Voyager")
            series_5 = Series(code="SNW", name="Star Trek: Strange New Worlds")

            session.add(series_1)
            session.add(series_2)
            session.add(series_3)
            session.add(series_4)
            session.add(series_5)

            session.commit()

            episode_1 = Episode(
                series_id=series_4.id, season=1, episode=11, title="State of Flux"
            )

            session.add(episode_1)
            session.commit()

            topic_1 = Topic(topic_name="cooking", episodes=[episode_1])
            session.add(topic_1)

            session.commit()
