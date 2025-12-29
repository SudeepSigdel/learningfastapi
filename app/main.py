from fastapi import FastAPI
# from . import database
from .routes import auth, user, post, vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.include_router(database.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(vote.router)


@app.get("/")
def index():
    return{"message":"Hello World"}