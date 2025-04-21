from fastapi import FastAPI
from .routers import episodes, series, topic

from .models import DB, SessionDep, engine

app = FastAPI()


@app.on_event("startup")
def on_startup():
    DB.init_db()
    # TODO, fix this dupe seeding
    DB.seed()


app.include_router(episodes.router)
app.include_router(series.router)
app.include_router(topic.router)
