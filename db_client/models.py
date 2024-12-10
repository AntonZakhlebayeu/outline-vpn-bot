from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text, create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class User(Base):
    """User scheme for storing the context of chatting"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=False)
    poland_key_id = Column(Integer, nullable=True)
    georgia_key_id = Column(Integer, nullable=True)
