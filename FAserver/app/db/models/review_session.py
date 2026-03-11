from app.db.core.base import *

class ReviewSession(Base):
    __tablename__ = "reviewsessions"

    id = Column(String(50), primary_key=True, autoincrement=False)
    userid = Column(String(50), ForeignKey("users.id"))
    createdat = Column(TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False)