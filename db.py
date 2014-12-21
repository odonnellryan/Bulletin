from peewee import MySQLDatabase, Model, CharField, IntegerField, TextField, DateTimeField, PrimaryKeyField
import datetime
database = MySQLDatabase(host='127.0.0.1', user='root', password='root', database='bulletin')

class Posts(Model):

    pk = PrimaryKeyField()
    title = CharField(255)
    content = TextField()
    posted_on = DateTimeField(default=datetime.datetime.now())
    rank = IntegerField()

    class Meta:
            database = database
