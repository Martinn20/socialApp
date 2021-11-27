from app.schemas import UserResponse, Token
from jose import jwt
from app.config import settings
import pytest

def test_create_user(client):
    res = client.post("/users/", json={"email": "moros2.toros@gmail.com", "password": "dasda1231fge"})
    new_user = UserResponse(**res.json())
    assert new_user.email == "moros2.toros@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    print(res.json())
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    email: str = payload.get("user_email")
    assert email == test_user['email']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ("wrong_email@gmail.com", "wrongpassord", 403),
    ("wrong_email@gmail.com", "dasda1231fge", 403),
    ("moros2.toros@gmail.com", "wrongpassord", 403),
    ("moros2.toros@gmail.com", None, 422),
    (None, "dasda1231fge", 422)])

def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
