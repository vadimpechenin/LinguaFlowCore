from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.schemas.word import WordCreate, WordRead, WordResponse, WordRecomendationResponse
from app.crud.word import create_word, list_words, list_words_duffuculty, get_word_by_id
from app.services.ml_client import recommend, get_ml_client
from app.services.ml_client import MLClient

router = APIRouter(prefix="/words", tags=["words"])


@router.get("", response_model=List[WordResponse])
def get_words(
    difficulty: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return list_words_duffuculty(db, difficulty, limit, offset)


@router.get("/", response_model=list[WordRead])
def list_all(db: Session = Depends(get_db), ml_client: MLClient = Depends(get_ml_client)):
    words = list_words(db)
    return list_words(db)


@router.get("/recommend", response_model=list[WordRecomendationResponse])#
async def recommend_words(user=Depends(get_current_user),
                    db: Session = Depends(get_db),
                    ml_client: MLClient = Depends(get_ml_client)):
    words = list_words(db)
    """
    result = ml_client.recommend(
        words
    )
    """
    result = await ml_client.recommend(
        words
    )

    if result is None:
        raise HTTPException(
            status_code=503,
            detail="ML Service unavailable"
        )

    return result

@router.get("/{word_id}", response_model=WordResponse)
def get_word(word_id: str, db: Session = Depends(get_db)):
    return get_word_by_id(db, word_id)


@router.post("", response_model=WordResponse)
def create_word(
    data: WordCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_word(db, data)


@router.post("/", response_model=WordRead)
def create(data: WordCreate, db: Session = Depends(get_db)):
    return create_word(db, data)


