from flask.ext import restful
from flask.ext.restful import fields
import db_mods
from web import app

api = restful.Api(app)

post_fields = {
            'id':   fields.Integer,
            'title': fields.String,
            'contents': fields.String,
            'rank': fields.Integer,
            'posted_on': fields.DateTime,
}

class Posts(restful.Resource):
    def get(self, id):
        post = db_mods.post_by_id(id)
        return fields.marshal(post,post_fields)

    def put(self, id, title, content, rank):
        return db_mods.update_post(id, title, content, rank)

    def delete(self, id):
        return db_mods.delete_post(id)

    def post(self, title, content, rank):
        return db_mods.new_post(title, content, rank)

class PostList(restful.Resource):

    def get(self, number_of_posts=10):
        posts =  db_mods.ranked_post_list(number_of_posts)
        post_dict = []
        for post in posts:
            post_dict.append(fields.marshal(post, post_fields))
        return post_dict


api.add_resource(Posts, '/post/', '/post/<int:id>/')
api.add_resource(PostList, '/post/list/', '/post/list/<int:number_of_posts>/')