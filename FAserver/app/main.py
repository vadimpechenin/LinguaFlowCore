# точка входа в сервер

from fastapi import FastAPI
from app.api import auth, users, words, progress, exams, settings, texts

app = FastAPI(title="English Learning API")

app.include_router(auth.router)
app.include_router(exams.router)
app.include_router(users.router)
app.include_router(words.router)
app.include_router(progress.router)
app.include_router(settings.router)
app.include_router(texts.router)