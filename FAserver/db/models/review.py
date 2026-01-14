from db.core.base import *

class WordReview(Base):
    __tablename__ = "wordreviews"

    id = Column(String(50), primary_key=True, autoincrement=False)

    userid = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    wordid = Column(
        String(50),
        ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False
    )

    reviewedat = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    iscorrect = Column(Boolean, nullable=False)
    responsetimems = Column(Integer)

    user = relationship("User", back_populates="wordreviews")
    word = relationship("Word", back_populates="reviews")
