from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(String, unique=True, index=True, nullable=False)
    reminder_time = Column(String, nullable=True)
    first_interaction_date = Column(Date, nullable=True)
    reminders_enabled = Column(Boolean, default=False, nullable=False)
