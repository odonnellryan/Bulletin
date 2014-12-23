from flask.ext import restful
from flask import session, g
from flask.ext.restful import fields
from web import app
import db_mods

api = restful.Api(app)


class Posts(restful.Resource):
    def get(self, pk):
        post = db_mods.find_post(pk)
        return fields.marshal(post, db_mods.post_fields)

    def put(self, pk, title, content, rank):
        return db_mods.update_post(pk, title, content, rank)

    def delete(self, pk):
        return db_mods.delete_post(pk)

    def post(self, title, content, rank):
        return db_mods.new_post(title, content, rank)


class Rank(restful.Resource):
    def put(self, pk, change=0):
        post_info = {str(pk): change}
        # simple way to not-so-securely handle multiple upvotes and downvotes.
        if not 'bulletin-rank-values' in session:
            session['bulletin-rank-values'] = post_info
            db_mods.change_rank(pk, int(change))
            return
        # needs to stringy the pk
        # JSON spec, etc.. etc..
        if str(pk) in session['bulletin-rank-values']:
            if session['bulletin-rank-values'][str(pk)] == change:
                # if they re-vote we want to remove their vote
                rank = int(change) * -1
                session['bulletin-rank-values'].pop(str(pk), None)
            else:
                # if they change their vote we have to double it to counter the previous vote.
                rank = int(change) * 2
                session['bulletin-rank-values'][str(pk)] = change
            db_mods.change_rank(pk, rank)
            return
        else:
            session['bulletin-rank-values'][str(pk)] = change
        db_mods.change_rank(pk, int(change))


class PostList(restful.Resource):
    def get(self, number_of_posts=10):
        return db_mods.ranked_post_details(number_of_posts)


api.add_resource(Posts, '/post/', '/post/<int:pk>/')
api.add_resource(PostList, '/post/list/', '/post/list/<int:number_of_posts>/')
api.add_resource(Rank, '/rank/<int:pk>/<string:change>/')