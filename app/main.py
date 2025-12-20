from fastapi import FastAPI
from .routers import user, post, auth
from . import database

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(database.router)
app.include_router(auth.router)