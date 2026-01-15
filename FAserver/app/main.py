# точка входа в сервер

from fastapi import FastAPI
from app.api import users, words, progress

app = FastAPI(title="English Learning API")

app.include_router(users.router)
app.include_router(words.router)
app.include_router(progress.router)