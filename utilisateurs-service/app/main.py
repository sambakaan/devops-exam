from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import auth, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="utilisateurs-service", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}
