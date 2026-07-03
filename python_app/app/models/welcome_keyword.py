"""
welcome_keyword.py

Stores voice activation phrases.
Example:
Vanga Sir
Enna Venum Sir
How can I help you
"""

from sqlalchemy import Column, Integer, String, Boolean

from app.core.database import Base



class WelcomeKeyword(Base):

    __tablename__ = "welcome_keywords"


    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    phrase = Column(
        String(255),
        nullable=False
    )


    language = Column(
        String(50),
        default="english"
    )


    action = Column(
        String(100),
        default="activate_voice"
    )


    enabled = Column(
        Boolean,
        default=True
    )


    def __repr__(self):

        return (
            f"<WelcomeKeyword "
            f"{self.phrase}>"
        )