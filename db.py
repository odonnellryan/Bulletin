import time

from peewee import Model, IntegerField, TextField, PrimaryKeyField, ForeignKeyField, BooleanField

import config


class MyModel(Model):
    class Meta:
        database = config.database


class User(MyModel):
    is_active = BooleanField(default=True)
    pk = PrimaryKeyField()
    social_id = IntegerField()
    username = TextField()
    role = TextField()


class Location(MyModel):
    pk = PrimaryKeyField()
    created_by = ForeignKeyField(User)
    title = TextField()
    description = TextField()


class Post(MyModel):
    pk = PrimaryKeyField()
    title = TextField()
    content = TextField()
    date = IntegerField(default=time.time())
    rank = IntegerField(default=0)
    # if hidden is 1 (true) the post won't be displayed
    hidden = IntegerField(default=0)
    points = IntegerField(default=0)
    created_by = ForeignKeyField(User)
    location = ForeignKeyField(Location)


class Votes(MyModel):

    UP = "up"
    DOWN = "down"

    pk = PrimaryKeyField()
    user = ForeignKeyField(User)
    post = ForeignKeyField(Post)
    type = TextField(default="None")


def create_tables():
    config.database.connect()
    config.database.create_tables([User, Location, Post, Votes])

#
# create_tables()
