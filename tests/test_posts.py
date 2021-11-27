import pytest

from app.schemas import PostOut, PostResponse

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_post_that_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/888888")
    assert res.status_code == 404

def test_user_get_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.user_id == test_posts[0].id

@pytest.mark.parametrize("title, content, published", [
    ("new title 1", "some content", True),
    ("new title 2", "some content22", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={'title': title, 'content': content, 'published': published})
    created_post = PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.user_id == test_user["id"]

def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={'title': "anunuada", 'content': "nandana"})
    created_post = PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == 'anunuada'
    assert created_post.content == "nandana"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]

def test_create_post_unauthorized_user(client, test_user):
    res = client.post("/posts/", json={'title': "anunuada", 'content': "nandana"})
    assert res.status_code == 401

def test_delete_post_unauthorized_user(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_that_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/99999009")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
            "title": "updateeeeee ",
            "content": "Molimm"
           }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updateeeeee ",
        "content": "Molimm",
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def update_post_that_does_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updateeeeee ",
        "content": "Molimm"
    }
    res = authorized_client.put(f"/posts/9999999", json=data)
    assert res.status_code == 404

def test_update_post_unauthorized_user(client, test_user, test_posts):
    data = {
        "title": "updateeeeee ",
        "content": "Molimm"
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_post_that_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updateeeeee ",
        "content": "Molimm"
    }
    res = authorized_client.put(f"/posts/99999009", json=data)
    assert res.status_code == 404