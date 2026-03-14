from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.crud.progress import seed_user_progress, create_progress_from_ids
from app.db.models import UserWordProgress
from app.schemas.word import WordCreate, WordRead, WordResponse, WordRecomendationResponse, WordID
from app.crud.word import create_word_by_data, list_words, list_words_duffuculty, get_word_by_id, \
    get_user_misssing_words
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
    return list_words(db)

@router.get("/available", response_model=list[WordResponse])
def get_available_words(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    words = get_user_misssing_words(db, user.id)

    return words


@router.get("/{word_id}", response_model=WordResponse)
def get_word(word_id: str, db: Session = Depends(get_db)):
    return get_word_by_id(db, word_id)


@router.post("", response_model=WordResponse)
def create_word(
    data: WordCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    word = create_word_by_data(db, data)
    result = seed_user_progress(
        db,
        user.id,
        [word.id],
        False
    )
    return word


@router.post("/from_table", response_model=list[WordRead])
async def create_word(
    data: List[WordCreate],
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    ml_client: MLClient = Depends(get_ml_client)
):
    #Загрузить все слова из базы
    base_words = list_words(db, limit = 100000)
    #Чисто слова
    base_texten = []
    new_texten = []
    for word in base_words:
        base_texten.append(word.texten)
    for word in data:
        new_texten.append(word.texten)
    #Выполнить сравнение, формальное
    unknown = set(new_texten).difference(
        set(base_texten)
    )
    #Индексы не известных слов
    #indexes = [i for i, x in enumerate(new_texten) if x in unknown]
    data_filtered = [x for x in data if x.texten in unknown]
    if (len(data_filtered)>0):
        new_texten=[]
        for word in data_filtered:
            new_texten.append(word.texten)
        #Выполнить сравнение с помощью кодировки
        result_unknown_words = await ml_client.get_new_words(
            base_texten, new_texten
        )
        #Список сохранить и добавить потом в progress пользователю
        data_filtered_ = [x for x in data_filtered if x.texten in result_unknown_words]
        result_words = []
        result_indexes = []
        for data_ in data_filtered_:
            if (len(data_.difficultylevel)>2):
                data_.difficultylevel = data_.difficultylevel[0:2]
            word = create_word_by_data(db, data_)
            result_words.append(word)
            result_indexes.append(word.id)
        result = seed_user_progress(
            db,
            user.id,
            result_indexes,
            False
        )
    else:
        result_words = []
    return result_words


@router.post("/add-to-progress")
async def add_words_to_progress(
    data: list[WordID],
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    res = create_progress_from_ids(db, data, user)

    return {"status": res}
