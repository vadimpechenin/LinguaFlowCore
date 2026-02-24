from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.api.deps import get_current_user
from app.api.deps import get_db
from app.core.settings import ML_SERVICE_URL
from app.db.models.text import Text
from app.schemas.text import TextResponse, TextRequest, TextAnalyzeResponse  # , TextAnalyzeResponse
from app.crud.text import create_text,get_text_by_title
from app.services.ml_client import get_ml_client, MLClient

router = APIRouter(prefix="/texts", tags=["Texts"])


@router.post("/", response_model=TextResponse)
async def submit_text(
    data: TextRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    text =create_text(db, user, data)
    return {"id": text.id,"title": text.title, "content": text.content}#, "questions": questions # ML


@router.get("/{text_title}", response_model=TextResponse)
async def load_text(
    text_title: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_text_by_title(db, text_title, user.id)

@router.post("/{text_title}/analyze", response_model=TextAnalyzeResponse)#
async def analyze(
    text_title: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
    ml_client: MLClient = Depends(get_ml_client)
):
    """
    Coverage  Level
    50%       Тяжело
    70%       Средне
    80%       Комфортно
    90%       Легко
    95%       Свободно

    :param examid:
    :param user:
    :param db:
    :return:
    """
    text = get_text_by_title(db, text_title, user.id)

    if not text:
        raise HTTPException(
            status_code=404,
            detail="Text not found"
        )

    result = await ml_client.analyze_text(
        text.content
    )

    return TextAnalyzeResponse(
        title=text_title,
        level=result["level"],
        unknown_words=result["unknown_words"],
        coveragepercent=result["coveragepercent"],
        recommended_words=result["recommended_words"]
    )




