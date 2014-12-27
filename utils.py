from datetime import datetime
import math

def parse_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%d %B %y')

def rank(rank, date):
    """The hot formula. Taken directly from reddit"""
    order = math.log((max(abs(rank), 1)),10)
    if rank > 0:
        sign = 1
    elif rank < 0:
        sign = -1
    else:
        sign = 0
    seconds = int(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)

def post_mods(posts, session_info):
    """
    take the posts dictionary and sort it based on the rank algorithm.
    we also need to do some date modifications and add the active/non-active css class metadata for the rank
    buttons to be properly handled
    the session_info is a dict of PKs and positive/negative/none associated ranks
    if positive, the positive rank is active, if negative the negative rank is active. else, none are active.
    """
    _posts = sorted(posts, key=lambda k: rank(k['rank'],k['date']), reverse=True)
    for post in _posts:
        post['date'] = parse_datetime(post['date'])
        if not session_info:
            post['down_active'] = "not-active"
            post['up_active'] = "not-active"
            continue
        if post['pk'] in session_info and session_info[post['pk']] == -1:
            post['down_active'] = "active"
        else:
            post['down_active'] = "not-active"
        if str(post['pk']) in session_info and session_info[post['pk']] == 1:
            post['up_active'] = "active"
        else:
            post['up_active'] = "not-active"
    return _posts