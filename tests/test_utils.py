from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database import Base
from database.models import Users, Data

from utils.autocorrect import autocorrect
from utils.json import jsonify_data_record



DATABASE_URL = "mysql+mysqlconnector://nkosinathiwalter:7MD!CUIJA[Av5DQh@localhost:3306/pixelscripttestdatabase"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def test_autocorrect():
    sentence1 = "Tesing if it works"
    sentence2 = "I am a sofwar develper"
    sentence3 = "I cn autocorrect sentnces and single wrds."
    
    result1 = autocorrect(sentence1)
    result2 = autocorrect(sentence2)
    result3 = autocorrect(sentence3)
    
    assert result1 == "\n\nTesting if it works"
    assert result2 == "\n\nI am a software developer"
    assert result3 == "\n\nI can autocorrect sentences and single words."


def test_jsonify_data_record():
    db = TestingSessionLocal()
    
    create_record = Data(text="this is inside of a testing function", headings=[], file_type="image/png", user_id=1)
    db.add(create_record)
    db.commit()
    db.refresh(create_record)

    record = db.query(Data).all()[0]
    
    result = jsonify_data_record(record=record)
    
    # jsonify_data_record basically changes date object to a string
    assert type(result['date']) == str
    
    db.delete(record)
    db.commit()
    db.close()
