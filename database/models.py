from .database import Base
from datetime import date

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text, Date
from sqlalchemy.dialects.mysql import JSON

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(Text, nullable=False)


class Data(Base):
    __tablename__ = "data"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    headings = Column(JSON)
    file_type = Column(String(10), nullable=False)
    date = Column(Date, nullable=False, default=date.today())
    
    user_id = Column(Integer, ForeignKey("users.id"))
