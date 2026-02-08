from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import httpx

from app.api.deps import get_current_user
from app.api.deps import get_db
from app.db.models.exam import Exam
from app.schemas.exam import ExamStart, ExamResponse, ExamResult
from app.crud.exam import create_exam

#TODO не реализована, еще делать и тестировать
ML_SERVICE_URL = "http://ml-api:8000"

router = APIRouter(prefix="/exam", tags=["Exams"])


@router.post("/start", response_model=ExamResponse)
async def start_exam(
    data: ExamStart,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    async with httpx.AsyncClient() as client:
        ml_resp = await client.post(
            f"{ML_SERVICE_URL}/ml/exam/start",
            json={
                "difficultylevel": data.difficulty,
                "size": data.size,
                "userid": user.id,
            },
        )
        ml_resp.raise_for_status()
        questions = ml_resp.json()["questions"]
    #TODO упаковать в crud
    exam = Exam(user_id=user.id, difficultylevel=data.difficulty)


    return {"examid": exam.id, "questions": questions}


@router.post("/{examid}/submit", response_model=ExamResult)
async def submit_exam(
    examid: int,
    payload: dict,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    async with httpx.AsyncClient() as client:
        ml_resp = await client.post(
            f"{ML_SERVICE_URL}/ml/exam/evaluate",
            json=payload,
        )
        ml_resp.raise_for_status()
        result = ml_resp.json()
    # TODO упаковать в crud
    exam = db.query(Exam).get(examid)
    exam.score = result["score"]
    db.commit()

    return result
