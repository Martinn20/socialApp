import pytest
from app.models import Vote


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_vote_on_already_voted_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409

def test_remove_vote_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201

def test_remove_vote_on_not_voted_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 404

def test_vote_on_post_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401

def test_vote_on_post_that_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 989989898, "dir": 1})
    assert res.status_code == 404