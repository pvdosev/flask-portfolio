from portfolio.db import init_app
from portfolio.models import db_wrapper


def test_init_close_db(app):
    with app.app_context():
        init_app(app)
        db_wrapper.database.close()
