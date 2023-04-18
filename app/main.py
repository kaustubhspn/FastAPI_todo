# Importing the required modules and packages.
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

from fastapi.middleware.cors import CORSMiddleware

# Creating the required database tables.
models.Base.metadata.create_all(bind=engine)

# Creating an instance of FastAPI class.
app = FastAPI()


#CORS Setup
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including the routers in the application.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Creating a root route for the application.
@app.get("/")
def root():
    """
    This function returns a simple message for the root route of the application.
    """

    return {"message": "Hello World"}
