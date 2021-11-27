from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Post, User
from app.database import get_db
from app.database import Base
import pytest
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:Ml050796.@localhost:5432/socialApp_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client, session):
    user_data = {"email": "moros2.toros@gmail.com", "password": "dasda1231fge"}
    res = client.post("/users/", json=user_data)

    user = session.query(User).filter(User.email == user_data["email"]).first()
    user = user.__dict__
    user['password'] = user_data['password']
    assert res.status_code == 201
    return user

@pytest.fixture
def test_user2(client, session):
    user_data = {"email": "joshh.toros@gmail.com", "password": "dasda1231fge"}
    res = client.post("/users/", json=user_data)

    user = session.query(User).filter(User.email == user_data["email"]).first()
    user = user.__dict__
    user['password'] = user_data['password']
    assert res.status_code == 201
    return user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_email": test_user['email']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [
        {
            "title": "papapapad ",
            "content": "Molimm",
            "user_id": test_user["id"]
        },
        {
            "title": "post 2 ",
            "content": "Molimmww2",
            "user_id": test_user["id"]
        },
        {
            "title": "Ps[pst] 3",
            "content": "Molimm33333",
            "user_id": test_user["id"]
        },
        {
            "title": "other user",
            "content": "Molimm33333",
            "user_id": test_user2["id"]
        }
    ]

    def create_post_model(p):
        return Post(**p)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()

    posts = session.query(Post).all()
    return posts