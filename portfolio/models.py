from peewee import AutoField, TextField, ForeignKeyField, TimestampField
from playhouse.flask_utils import FlaskDB

db_wrapper = FlaskDB()


class User(db_wrapper.Model):
    user_id = AutoField(primary_key=True)
    username = TextField(unique=True)
    password = TextField()


class Post(db_wrapper.Model):
    title = TextField()
    slug = TextField(primary_key=True, unique=True)
    blurb = TextField()
    author_id = ForeignKeyField(model=User, backref="posts")
    created = TimestampField()
    path = TextField(unique=True)
