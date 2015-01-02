from api import app
from flask import g, session
import utils
import config
import db_mods
import db
# TODO: not this, don't do this, not that it matters much for this app.
app.secret_key = 'super_secret_session_key'

@app.context_processor
def inject_urls():
    """
    sets variables that are used in each view. the g-based variables are already passed to the view, so these can
    be factored out, but i left them like this for now.
    """
    return dict(company_name=config.company_name)

@app.before_request
def before_request():
    """
        before request
    """
    if not 'posts' in session:
        session_info = session.get('bulletin-rank-values') or None
        session['posts'] = utils.post_mods(db_mods.ranked_post_details(), session_info)
    try:
        g.db = config.database
        g.db.connect()
    # this can return any number of sql exceptions
    except Exception as e:
        print('DB BROKE')
        return e

@app.teardown_request
def teardown_request(exception):
    g.db.close()

if __name__ == '__main__':
    app.run(debug=True)