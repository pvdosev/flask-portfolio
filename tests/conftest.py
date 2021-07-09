import os
import tempfile

import pytest
from portfolio import create_app
from portfolio.db import init_db
from portfolio.models import Post, User, db_wrapper


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": "sqliteext:///%s" % db_path,
            "SECRET_KEY": "test",
        }
    )

    with app.app_context():
        init_db()
        User.create(
            username="test",
            password="pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f",
        )
        User.create(
            username="other",
            password="pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79",
        )
        Post.create(
            slug="test",
            title="Test!",
            blurb="body",
            path="/this/doesnt/work/yet",
            author_id=1,
        )

        db_wrapper.database.close()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
