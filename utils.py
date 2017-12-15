import math
from datetime import datetime

from db import Votes


class Pagination:
    def __init__(self, per_page, posts, page):
        self.page = page
        self.per_page = per_page
        self.total_count = len(posts)
        self.posts = posts

    @property
    def pages(self):
        return int(math.ceil(self.total_count / float(self.per_page)))

    @property
    def prev_page(self):
        if (self.page - 1) >= 1:
            return self.page - 1
        return None

    @property
    def next_page(self):
        if (self.page + 1) <= self.pages:
            return self.page + 1
        return None

    @property
    def posts_by_page(self):
        # first page is really page 0, etc.
        start_post = (self.page - 1) * self.per_page
        end_post = start_post + self.per_page
        return self.posts[start_post:end_post]


def parse_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%d %B %y')


def rank(rank, date):
    """The hot formula. Taken directly from reddit"""
    order = math.log((max(abs(rank), 1)), 10)
    if rank > 0:
        sign = 1
    elif rank < 0:
        sign = -1
    else:
        sign = 0
    seconds = int(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)


def post_mods(posts, current_user):
    """
    take the posts dictionary and sort it based on the rank algorithm.
    we also need to do some date modifications and add the active/non-active css class metadata for the rank
    buttons to be properly handled
    the session_info is a dict of PKs and positive/negative/none associated ranks
    if positive, the positive rank is active, if negative the negative rank is active. else, none are active.
    """
    votes = Votes.select().where(Votes.user == current_user.pk)
    user_votes = {str(vote.post.pk): vote.type for vote in votes}
    _posts = sorted(posts, key=lambda k: rank(k['rank'], k['date']), reverse=True)
    for post in _posts:
        post['date'] = parse_datetime(post['date'])
        if post['pk'] in user_votes:
            type = user_votes[post['pk']]
            if type == Votes.UP:
                post['up_active'] = "active"
                post['down_active'] = "not-active"
            elif type == Votes.DOWN:
                post['down_active'] = "active"
                post['up_active'] = "not-active"
            else:
                post['down_active'] = "not-active"
                post['up_active'] = "not-active"
    return _posts
