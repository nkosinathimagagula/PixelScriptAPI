from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+mysqlconnector://nkosinathiwalter:7MD!CUIJA[Av5DQh@localhost:3306/pixelscript"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
