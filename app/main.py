from app.config import settings
from .database import engine
from fastapi import FastAPI
from . import models
from .routers import post, user, auth


print(settings.database_password)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Hello World"}
