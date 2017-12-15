from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask.ext.login import login_user
from flask_login import LoginManager
from flask_oauthlib.client import OAuth

import config
import db
import db_mods
from api import app

# TODO: not this, don't do this, not that it matters much for this app.
app.secret_key = 'super_secret_session_key'

FACEBOOK_APP_ID = '1369632986496593'
FACEBOOK_APP_SECRET = 'e8b867fcd5c696500907522ee363bf93'

oauth = OAuth()
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = "login"

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': 'email'}
                            )


def create_tables():
    database = config.database
    database.connect()
    print(db.Post.create_table())


@app.context_processor
def inject_urls():
    """
    sets variables that are used in each view. the g-based variables are already passed to the view, so these can
    be factored out, but i left them like this for now.
    """
    return dict(company_name=config.company_name)


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = db_mods.get_or_create_user(me)
    login_user(user)
    return redirect(url_for('main'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@login_manager.user_loader
def load_user(userid):
    return db.User(pk=userid)


if __name__ == '__main__':
    app.run(debug=True)
