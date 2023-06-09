from fastapi import status
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db

from database.database import Base
from database.models import Users


DATABASE_URL = "mysql+mysqlconnector://nkosinathiwalter:7MD!CUIJA[Av5DQh@localhost:3306/pixelscripttestdatabase"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


client = TestClient(app=app)


def overide_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        

app.dependency_overrides[get_db] = overide_get_db


# testing the test connection endpoint ------------------------------
def test_home():
    response = client.get("/")
    
    data = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert data['status_code'] == status.HTTP_200_OK
    assert data['message'] == "success"
# -------------------------------------------------------------------


# test generating the access token for an existing user in the database
def test_generate_access_token():
    response = client.post(
        "/token",
        data={
            "username": "test@test.com",
            "password": "test"
        },
        headers={
            "content-type": "application/x-www-form-urlencoded"
        }
    )
    
    data = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert type(data['access_token']) == str
    assert len(data['access_token']) != 0
    assert data['token_type'] == "bearer"


# test generating the access token for a user not in the database
def test_generate_access_token_for_non_user():
    response = client.post(
        "/token",
        data={
            "username": "non@user.com",
            "password": "nonuserpassword"
        },
        headers={
            "content-type": "application/x-www-form-urlencoded"
        }
    )
    
    data = response.json()
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert data['detail'] == "Invalid username/email or password"
    

# test creating a user
def test_create_user():
    response = client.post(
        "/api/PST/users/",
        json={
            "name": "unittest",
            "email": "unit@test.com",
            "password": "unittest"
        }
    )
    
    data = response.json()
    
    assert response.status_code == status.HTTP_201_CREATED
    assert data['detail'] == "user created"
    
    
    db = TestingSessionLocal()
    created_user = db.query(Users).filter(Users.email == "unit@test.com").first()
    db.delete(created_user)
    db.commit()
    

# test reading data from the database
def test_read_data():
    token_gen_response = client.post(
        "/token",
        data={
            "username": "test@test.com",
            "password": "test"
        },
        headers={
            "content-type": "application/x-www-form-urlencoded"
        }
    )
    
    access_token = token_gen_response.json()['access_token']
    
    response = client.get(
        "/api/PST/extract/data/",
        headers={
            "accept": "application/json",
            "Authorization": "Bearer " + access_token
        }
    )
    
    data = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert type(data) == list
