from app.db.core.base import *


class ExamResult(Base):
   __tablename__ = "examresults"

   id = Column(String(50), primary_key=True, autoincrement=False)
   examid = Column(
        String(50),
        ForeignKey("exams.id", ondelete="CASCADE")
    )
   userid = Column(String(50))
   score = Column(Integer)
   estimatedlevel = Column(String(10))
