from app.db.core.base import *

class Exam(Base):
    __tablename__ = "exams"

    id = Column(String(50), primary_key=True, autoincrement=False)
    userid = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    difficultylevel = Column(String(2))
    size = Column(Integer)

    takenat = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="exams")
