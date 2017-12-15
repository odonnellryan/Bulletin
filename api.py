import flask_restful
from flask import request
from flask.ext.restful import fields
from flask_login import current_user
from playhouse.shortcuts import model_to_dict

import db_mods
from db import Votes, Post
from web import app

api = flask_restful.Api(app)


class Posts(flask_restful.Resource):
    def get(self, pk):
        post = db_mods.find_post(pk)
        return fields.marshal(post, db_mods.post_fields)

    def put(self, pk):
        try:
            _ = Post.get(Post.created_by == current_user.pk, Post.pk == pk)
        except Post.DoesNotExist:
            return {'error': 'You do not have permission to do that. '}
        return db_mods.edit_post(pk, request.form['title'], request.form['content'], request.form['points'])

    def delete(self, pk):
        try:
            _ = Post.get(Post.created_by == current_user.pk, Post.pk == pk)
        except Post.DoesNotExist:
            return {'error': 'You do not have permission to do that. '}
        return db_mods.delete_post(pk)

    def post(self):
        post = db_mods.new_post(request.form['title'], request.form['content'], request.form['points'], current_user)
        return model_to_dict(post)


class Rank(flask_restful.Resource):
    def get(self, pk):
        if db_mods.find_post(pk):
            return int(db_mods.find_post(pk).rank)
        return None

    def put(self, pk, change=0):
        change = int(change)
        pk = int(pk)
        vote, _ = Votes.get_or_create(post=pk, user=current_user.pk)
        if vote.type == Votes.UP:
            if change == 1:
                change = -1
                vote.type = "None"
            elif change == -1:
                change = -2
                vote.type = Votes.DOWN
        elif vote.type == Votes.DOWN:
            if change == -1:
                change = +1
                vote.type = "None"
            elif change == 1:
                change = 2
                vote.type = Votes.UP
        else:
            if change > 0:
                vote.type = Votes.UP
            elif change < 0:
                vote.type = Votes.DOWN

        vote.save()

        db_mods.change_rank(pk, change)


class PostList(flask_restful.Resource):
    def get(self, number_of_posts=10):
        return db_mods.ranked_post_details(number_of_posts)


api.add_resource(Posts, '/post/', '/post/<int:pk>/')
api.add_resource(PostList, '/post/list/', '/post/list/<int:number_of_posts>/')
api.add_resource(Rank, '/rank/<string:pk>/', '/rank/<string:pk>/<string:change>/')
