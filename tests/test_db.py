import pytest
import peewee
from portfolio.db import init_app
from portfolio.models import db_wrapper


def test_model_proxy_db():
    assert type(db_wrapper.database) is peewee.Proxy
    assert db_wrapper.database.is_closed() is True

def test_init_close_db(app):
    with app.app_context():
        init_app(app)
        db_wrapper.database.close()