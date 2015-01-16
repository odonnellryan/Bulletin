from flask.ext.restful import fields

import db


post_fields = {
    # this is going to be a key, might as well keep it a string
    'pk': fields.String,
    'title': fields.String,
    'content': fields.String,
    'rank': fields.Integer,
    'date': fields.Integer,
}

Posts = db.Posts


def ranked_post_details():
    db_posts = Posts.select().where(Posts.hidden == 0)
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
    post = Posts.update(hidden=1).where(Posts.pk == pk)
    return post.execute()


def change_rank(pk, change):
    post = Posts.update(rank=Posts.rank + change).where(Posts.pk == pk)
    return post.execute()


def edit_post(pk, title, content, rank):
    post = Posts.update(title=title, content=content, rank=rank).where(Posts.pk == pk)
    return post.execute()