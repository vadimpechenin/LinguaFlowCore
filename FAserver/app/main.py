# точка входа в сервер

from fastapi import FastAPI
from app.api import auth, users, words, progress, exams, settings, texts
from fastapi.middleware.cors import CORSMiddleware


#if __name__=="__main__":
app = FastAPI(title="English Learning API")

#Блок добавления связи с фронтэндом
origins = [
    #"http://localhost:5173",
    #"http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Все пути
app.include_router(auth.router)
app.include_router(exams.router)
app.include_router(users.router)
app.include_router(words.router)
app.include_router(progress.router)
app.include_router(settings.router)
app.include_router(texts.router)