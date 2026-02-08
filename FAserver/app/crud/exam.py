from sqlalchemy.orm import Session

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import Exam


def create_exam(db: Session, data) -> Exam:
    ID = UUIDClass.geterateUUIDWithout_()
    exam = Exam(**data.dict())
    exam.id = ID
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam
