import pytest
from portfolio.models import Post


def test_index(client, auth):
    response = client.get("/blog")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/blog")
    assert b"Log Out" in response.data
    assert b"Test!" in response.data
    assert b"by test" in response.data
    assert b"body" in response.data
    assert b'href="/test/update"' in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/test/update",
        "/test/delete",
    ),
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "http://localhost/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user

    auth.login("other", "other")
    # current user can't modify other user's post
    assert client.post("/test/update").status_code == 403
    assert client.post("/test/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/test/update"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/blah/update",
        "/blah/delete",
    ),
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "Wow! A test", "body": ""})

    with app.app_context():
        count = Post.select().count()
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/test/update").status_code == 200
    client.post("/test/update", data={"title": "updated", "body": ""})

    with app.app_context():
        # TODO: This test will stop working as soon as slug editing is allowed
        post = Post.get_or_none(Post.slug == "test")
        assert post.title == "updated"


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/test/update",
    ),
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/test/delete")
    assert response.headers["Location"] == "http://localhost/blog"

    with app.app_context():
        post = Post.get_or_none(Post.slug == "test")
        assert post is None
