import db
from flask.ext.restful import fields
from datetime import datetime

class UrgentItem(fields.Raw):
    def format(self, value):
        return "Urgent" if value & 0x01 else "Normal"

post_fields = {
            'id':   fields.Integer,
            'title': fields.String,
            'content': fields.String,
            'rank': fields.Integer,
            'posted_on': fields.DateTime,
}



Posts = db.Posts

def ranked_post_details(number):
    db_posts = Posts.select().order_by(Posts.rank.desc()).limit(number)
    post_details = [fields.marshal(post, post_fields) for post in db_posts]
    return post_details

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
    return post.execute()