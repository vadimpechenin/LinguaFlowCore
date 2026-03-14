from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.deps import get_db
from app.db.models import UserSettings
from app.schemas.exam import ExamStart, ExamResponse, ExamResult, ExamSubmit, ExamResponseAllFields
from app.crud.exam import ExamService

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.get("", response_model=List[ExamResponseAllFields])
async def get_exam(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    :param data:
    :param user:
    :param db:
    :return:
    """
    service = ExamService()
    settings = db.query(UserSettings).filter(UserSettings.userid == user.id).first()
    exams = service.get_exams(
        db,
        user.id,settings.dailywordlimit*2
    )
    result = []
    for item in exams:
        result.append({ "id" : item.id,
                        "userid" : item.userid,
                        "difficultylevel": item.difficultylevel,
                        "size": item.size,
                        "takenat": item.takenat})

    return result
@router.post("/start", response_model=ExamResponse)
async def start_exam(
    data: ExamStart,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    :param data:
    :param user:
    :param db:
    :return:
    """
    service = ExamService()
    return service.start_exam(
        db,
        user.id,
        data.difficultylevel,
        data.size
    )


@router.post("/{exam_id}/submit", response_model=ExamResult)
async def submit_exam(
    exam_id: str,
    payload: ExamSubmit,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ExamService()
    result = service.submit_exam(
        db,
        exam_id,
        user.id,
        payload.answers
    )
    return result

