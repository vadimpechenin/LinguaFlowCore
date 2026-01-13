from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas.word import WordCreate, WordRead
from crud.word import create_word, list_words

router = APIRouter(prefix="/words", tags=["words"])


@router.post("/", response_model=WordRead)
def create(data: WordCreate, db: Session = Depends(get_db)):
    return create_word(db, data)


@router.get("/", response_model=list[WordRead])
def list_all(db: Session = Depends(get_db)):
    return list_words(db)