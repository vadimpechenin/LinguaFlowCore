from db.core.base import *

class UserSettings(Base):
    __tablename__ = "usersettings"

    userid = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    interfacelanguage = Column(String(10), nullable=False, default="ru")
    learninglanguage = Column(String(10), nullable=False, default="en")
    preferredvoice = Column(String(50))
    dailywordlimit = Column(Integer, nullable=False, default=20)
    enableaudio = Column(Boolean, nullable=False, default=True)
    enablenotifications = Column(Boolean, nullable=False, default=True)
    timezone = Column(String(50), nullable=False, default="UTC")

    user = relationship("User", back_populates="settings")
