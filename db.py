from peewee import MySQLDatabase, Model, CharField, IntegerField, TextField, DateTimeField, PrimaryKeyField
import datetime
database = MySQLDatabase('127.0.0.1', user='root', password='root')

class Posts(Model):

    id = PrimaryKeyField(11)
    title = CharField(255)
    contents = TextField()
    posted_on = DateTimeField(default=datetime.datetime.now())
    weighted_rank = IntegerField()

    class Meta:
            database = database
