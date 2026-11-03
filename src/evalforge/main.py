from fastapi import FastAPI

from .db.database import Base, engine
from .db import models  # noqa: F401  (registers the tables)
from .routers import apps

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EvalForge", version="0.1.0")
app.include_router(apps.router)


@app.get("/health")
def health():
    return {"status": "ok"}