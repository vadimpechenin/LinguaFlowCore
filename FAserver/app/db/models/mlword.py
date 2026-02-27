from app.db.core.base import *

class MLWordFeatures(Base):
    __tablename__ = "mlwordfeatures"

    wordid = Column(
        String(50),
        ForeignKey("words.id", ondelete="CASCADE"),
        primary_key=True
    )

    frequencyrank = Column(Integer)
    avgsuccessrate = Column(Float)
    avgreviewinterval = Column(Float)

    word = relationship("Word", back_populates="mlfeatures")
