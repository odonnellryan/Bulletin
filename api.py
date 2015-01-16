from flask.ext import restful
from flask import session, g, request
from flask.ext.restful import fields
from web import app
import db_mods

api = restful.Api(app)


class Posts(restful.Resource):
    def get(self, pk):
        post = db_mods.find_post(pk)
        return fields.marshal(post, db_mods.post_fields)

    def put(self, pk):
        return db_mods.edit_post(pk, request.form['title'], request.form['content'], request.form['rank'])

    def delete(self, pk):
        return db_mods.delete_post(pk)

    def post(self):
        return db_mods.new_post(request.form['title'], request.form['content'], request.form['rank'])


class Rank(restful.Resource):

    def get(self, pk):
        if db_mods.find_post(pk):
            return int(db_mods.find_post(pk).rank)
        return None

    def put(self, pk, change=0):
        change = int(change)
        post_info = {pk: change}
        # simple way to not-so-securely handle multiple upvotes and downvotes.
        if not 'bulletin-rank-values' in session:
            session['bulletin-rank-values'] = post_info
            db_mods.change_rank(pk, change)
            return
        if pk in session['bulletin-rank-values']:
            if session['bulletin-rank-values'][pk] == change:
                # if they re-vote we want to remove their vote
                rank = change * -1
                session['bulletin-rank-values'].pop(pk, None)
            else:
                # if they change their vote we have to double it to counter the previous vote.
                rank = change * 2
                session['bulletin-rank-values'][pk] = change
            db_mods.change_rank(pk, rank)
            return
        else:
            session['bulletin-rank-values'][pk] = change
        db_mods.change_rank(pk, change)


class PostList(restful.Resource):
    def get(self, number_of_posts=10):
        return db_mods.ranked_post_details(number_of_posts)


api.add_resource(Posts, '/post/', '/post/<int:pk>/')
api.add_resource(PostList, '/post/list/', '/post/list/<int:number_of_posts>/')
api.add_resource(Rank, '/rank/<string:pk>/', '/rank/<string:pk>/<string:change>/')