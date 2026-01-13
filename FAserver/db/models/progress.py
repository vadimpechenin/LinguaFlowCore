from core.base import *

class UserWordProgress(Base):
    __tablename__ = "userwordprogress"

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

    lastreviewedat = Column(TIMESTAMP(timezone=True))
    nextreviewat = Column(TIMESTAMP(timezone=True))

    successrate = Column(Float, nullable=False, default=0.0)
    reviewcount = Column(Integer, nullable=False, default=0)
    isknown = Column(Boolean, nullable=False, default=False)

    createdat = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="wordprogress")
    word = relationship("Word", back_populates="userprogress")

    from sqlalchemy import UniqueConstraint
    __table_args__ = (
        UniqueConstraint("userid", "wordid", name="uquserword"),
    )

