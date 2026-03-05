from sqlalchemy.orm import Session

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import Exam, User, Word
from app.db.models.examresult import ExamResult
from app.services.pipelines.exam_generator import ExamGenerator
from app.services.pipelines.level_extimator import LevelEstimator


class ExamService:

   def __init__(self):
       self.generator = ExamGenerator()
       self.estimator = LevelEstimator()

   # 1 START
   def start_exam(self, db: Session, user_id: str, difficulty: str, size: int):

       words = (
           db.query(Word)
           .filter(Word.difficultylevel == difficulty)
           .all()
       )

       exam = Exam(
           id=UUIDClass.geterateUUIDWithout_(),
           userid=user_id,
           difficultylevel=difficulty,
           size=size
       )

       db.add(exam)
       db.commit()
       db.refresh(exam)

       questions = self.generator.generate(words, size)

       return {
           "examid": exam.id,
           "questions": questions
       }

   # 2 SUBMIT
   def submit_exam(self, db: Session, exam_id: str, user_id: str, answers: list):

       exam = db.query(Exam).filter(Exam.id == exam_id).first()

       correct = sum(1 for a in answers if a["is_correct"])
       total = len(answers)

       score_percent = int((correct / total) * 100)

       estimated = self.estimator.estimate(
           exam.difficultylevel,
           score_percent
       )

       result = ExamResult(
           id=UUIDClass.geterateUUIDWithout_(),
           examid=exam_id,
           userid=user_id,
           score=score_percent,
           estimatedlevel=estimated
       )

       db.add(result)
       db.commit()

       return {
           "score": score_percent,
           "estimatedlevel": estimated
       }

   def get_exams(self, db: Session, user_id: str, limit: int):

       return (
           db.query(Exam)
           .filter(Exam.userid == user_id)
           .limit(limit).all()
       )
