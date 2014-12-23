from api import app
from flask import g
from peewee import OperationalError
import db

app.secret_key = 'super_secret_session_key'

@app.before_request
def before_request():
    """
        before request
    """
    try:
        g.db = db.database
        g.db.connect()
    # this can return any number of sql exceptions
    except Exception as e:
        return e

@app.teardown_request
def teardown_request(exception):
    g.db.close()

if __name__ == '__main__':
    app.run(debug=True)