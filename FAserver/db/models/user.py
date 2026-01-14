from db.core.base import *

class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, autoincrement=False)
    name = Column(String(50))
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    initiallevel = Column(String(50))
    createdat = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    lastloginat = Column(TIMESTAMP(timezone=True))
    isactive = Column(Boolean, nullable=False, default=True)

    settings = relationship(
        "UserSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    wordprogress = relationship(
        "UserWordProgress",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    wordreviews = relationship(
        "WordReview",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    texts = relationship(
        "Text",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    exams = relationship(
        "Exam",
        back_populates="user",
        cascade="all, delete-orphan"
    )
