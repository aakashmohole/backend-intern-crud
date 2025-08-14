from fastapi import FastAPI
from src.api import posts, auth
from src.db.database import engine, Base

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
