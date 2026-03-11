from app.db.core.base import *

class ReviewSessionWord(Base):
    __tablename__ = "reviewsessionswords"

    id = Column(String(50), primary_key=True, autoincrement=False)
    sessionid = Column(String(50), ForeignKey("reviewsessions.id"))
    wordid = Column(String(50),ForeignKey("words.id"))