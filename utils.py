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

def sort_by_rank(posts):
    _posts = sorted(posts, key=lambda k: rank(k['rank'],k['date']), reverse=True)
    for post in _posts:
        post['date'] = parse_datetime(post['date'])
    return _posts