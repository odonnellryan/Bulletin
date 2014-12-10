import db

Posts = db.Posts

def ranked_post_list(number):
    return Posts.select().order_by(Posts.rank.desc()).limit(number)

def post_by_id(id):
    return Posts.get(Posts.id == id)

def new_post(title, content, rank):
    insert_post = Posts()
    insert_post.title = title
    insert_post.content = content
    insert_post.rank = rank
    insert_post.save()
    return insert_post.id

def delete_post(id):
    post = Posts.get(Posts.id == id)
    return post.delete_instance()

def update_post(id, title, contents, weighted_rank):
    post = Posts.update(title = title, contents = contents, weighted_rank = weighted_rank).where(id == id)
    post.execute()