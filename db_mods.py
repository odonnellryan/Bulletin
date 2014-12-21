import db
from flask.ext.restful import fields
from datetime import datetime

class CustomTime(fields.Raw):
    def format(self, value):
        return value.strftime('%d %B %y')

post_fields = {
            'pk':   fields.Integer,
            'title': fields.String,
            'content': fields.String,
            'rank': fields.Integer,
            'posted_on': CustomTime,
}

Posts = db.Posts

def ranked_post_details(number):
    db_posts = Posts.select().order_by(Posts.rank.desc()).limit(number)
    post_details = [fields.marshal(post, post_fields) for post in db_posts]
    return post_details

def post_by_pk(pk):
    return Posts.get(Posts.pk == pk)

def new_post(title, content, rank):
    insert_post = Posts()
    insert_post.title = title
    insert_post.content = content
    insert_post.rank = rank
    insert_post.save()
    return insert_post.pk

def delete_post(pk):
    post = Posts.get(Posts.pk == pk)
    return post.delete_instance()

def update_post(pk, title, contents, weighted_rank):
    post = Posts.update(title = title, contents = contents, weighted_rank = weighted_rank).where(pk == pk)
    return post.execute()