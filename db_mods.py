import db
from flask.ext.restful import fields
from datetime import datetime

post_fields = {
    # this is going to be a key, might as well keep it a string
    'pk': fields.String,
    'title': fields.String,
    'content': fields.String,
    'rank': fields.Integer,
    'date': fields.Integer,
}

Posts = db.Posts


def ranked_post_details(number):
    db_posts = Posts.select().limit(number)
    post_details = [fields.marshal(post, post_fields) for post in db_posts]
    return post_details


def find_post(pk):
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


def change_rank(pk, change):
    post = Posts.update(rank=Posts.rank + change).where(Posts.pk == pk)
    return post.execute()


def update_post(pk, title, contents, weighted_rank):
    post = Posts.update(title=title, contents=contents, weighted_rank=weighted_rank).where(Posts.pk == pk)
    return post.execute()