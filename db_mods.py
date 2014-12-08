import db

Posts = db.Posts

def ranked_post_list(number=100):
    Posts.select()

def post_post(title, contents, weighted_rank):

    insert_post = Posts()
