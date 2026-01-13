from core.base import *

class TextVocabularyStats(Base):
    __tablename__ = "textvocabularystats"

    id = Column(String(50), primary_key=True, autoincrement=False)
    textid = Column(
        String(50),
        ForeignKey("texts.id", ondelete="CASCADE"),
        nullable=False
    )

    totalwords = Column(Integer, nullable=False)
    knownwords = Column(Integer, nullable=False)
    unknownwords = Column(Integer, nullable=False)
    coveragepercent = Column(Float, nullable=False)

    computedat = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    text = relationship("Text", back_populates="vocabularystats")
