from db.core.base import *

class Word(Base):
    __tablename__ = "words"

    id = Column(String(50), primary_key=True, autoincrement=False)
    texten = Column(String(100), nullable=False)
    transcription = Column(String(100))
    textl = Column(String(100))
    partofspeech = Column(String(50))
    examplesentence = Column(String(500))
    difficultylevel = Column(String(2), nullable=False)
    audiourl = Column(String(500))

    createdat = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    userprogress = relationship(
        "UserWordProgress",
        back_populates="word",
        cascade="all, delete-orphan"
    )

    reviews = relationship(
        "WordReview",
        back_populates="word",
        cascade="all, delete-orphan"
    )

    mlfeatures = relationship(
        "MLWordFeatures",
        back_populates="word",
        uselist=False,
        cascade="all, delete-orphan"
    )
