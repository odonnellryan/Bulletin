from flask.ext import restful
from flask.ext.restful import fields
from web import app
import db_mods

api = restful.Api(app)

class Posts(restful.Resource):
    def get(self, pk):
        post = db_mods.post_by_pk(pk)
        return fields.marshal(post,db_mods.post_fields)

    def put(self, pk, title, content, rank):
        return db_mods.update_post(pk, title, content, rank)

    def delete(self, pk):
        return db_mods.delete_post(pk)

    def post(self, title, content, rank):
        return db_mods.new_post(title, content, rank)

class PostList(restful.Resource):
    def get(self, number_of_posts=10):
        return db_mods.ranked_post_details(number_of_posts)


api.add_resource(Posts, '/post/', '/post/<int:pk>/')
api.add_resource(PostList, '/post/list/', '/post/list/<int:number_of_posts>/')