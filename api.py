from flask.ext import restful
from web import app

api = restful.Api(app)

class Posts(restful.Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Posts, '/posts')