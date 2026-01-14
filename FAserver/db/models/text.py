from db.core.base import *

class Text(Base):
    __tablename__ = "texts"

    id = Column(String(50), primary_key=True, autoincrement=False)
    userid = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(10), nullable=False, default="en")

    createdat = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="texts")
    vocabularystats = relationship(
        "TextVocabularyStats",
        back_populates="text",
        uselist=False,
        cascade="all, delete-orphan"
    )
