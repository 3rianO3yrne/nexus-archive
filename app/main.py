from fastapi import FastAPI
from .routers import episodes, series

from .models import DB

app = FastAPI()


@app.on_event("startup")
def on_startup():
    DB.init_db()


app.include_router(episodes.router)
app.include_router(series.router)
