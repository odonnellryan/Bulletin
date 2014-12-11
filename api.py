from flask.ext import restful
from flask.ext.restful import fields
from web import app
import db_mods

api = restful.Api(app)

class Posts(restful.Resource):
    def get(self, id):
        post = db_mods.post_by_id(id)
        return fields.marshal(post,db_mods.post_fields)

    def put(self, id, title, content, rank):
        return db_mods.update_post(id, title, content, rank)

    def delete(self, id):
        return db_mods.delete_post(id)

    def post(self, title, content, rank):
        return db_mods.new_post(title, content, rank)

class PostList(restful.Resource):
    def get(self, number_of_posts=10):
        return db_mods.ranked_post_details(number_of_posts)


api.add_resource(Posts, '/post/', '/post/<int:id>/')
api.add_resource(PostList, '/post/list/', '/post/list/<int:number_of_posts>/')