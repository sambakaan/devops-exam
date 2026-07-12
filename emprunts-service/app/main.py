from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import emprunts


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="emprunts-service", lifespan=lifespan)

app.include_router(emprunts.router)


@app.get("/health")
def health():
    return {"status": "ok"}
