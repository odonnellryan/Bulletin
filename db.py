from peewee import Model, CharField, IntegerField, TextField, PrimaryKeyField
import time
import config

class Posts(Model):

    pk = PrimaryKeyField()
    title = CharField(255)
    content = TextField()
    date = IntegerField(default=time.time())
    rank = IntegerField(default=0)
    # if hidden is 1 (true) the post won't be displayed
    hidden = IntegerField(default=0)

    class Meta:
        database = config.database
