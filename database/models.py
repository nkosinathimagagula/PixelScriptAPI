from .database import Base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text, Date

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(20), nullable=False)


class Data(Base):
    __tablename__ = "data"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    file_type = Column(String(10), nullable=False)
    date = Column(Date, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"))
