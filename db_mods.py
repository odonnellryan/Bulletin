from flask.ext.restful import fields

from db import User, Post, Location, Votes

post_fields = {
    # this is going to be a key, might as well keep it a string
    'pk': fields.String,
    'title': fields.String,
    'content': fields.String,
    'rank': fields.Integer,
    'points': fields.Integer,
    'date': fields.Integer,
}


def ranked_post_details(number_of_posts=None):
    db_posts = Post.select().where(Post.hidden == 0)
    post_details = [fields.marshal(post, post_fields) for post in db_posts]
    if number_of_posts:
        return post_details[number_of_posts:]
    else:
        return post_details


def find_post(pk):
    return Post.get(Post.pk == pk)


def get_or_create_location(user, location_name, location_description):
    location, _ = Location.get_or_create(title=location_name,
                                         defaults={'created_by': user.pk, 'description': location_description})
    return location


def new_post(title, content, points, user, location=None):
    if location is None:
        location = get_or_create_location(user, 'default', 'A catch-all location. Generic stuff here ... ')
    else:
        location = get_or_create_location(user, **location)
    insert_post = Post.create(title=title, content=content, points=points, created_by_id=user.pk, rank=1,
                              location_id=location.pk)
    return insert_post


def delete_post(pk):
    post = Post.update(hidden=1).where(Post.pk == pk)
    _ = delete_post_votes(pk)
    return post.execute()


def delete_post_votes(pk):
    votes = Votes.delete().where(Votes.post == pk)
    return votes.execute()


def change_rank(pk, change):
    post = Post.update(rank=Post.rank + change).where(Post.pk == pk)
    return post.execute()


def edit_post(pk, title, content, points):
    post = Post.update(title=title, content=content, points=points).where(Post.pk == pk)
    return post.execute()


def get_user(user_social_id):
    try:
        return User.get(User.social_id == user_social_id)
    except User.DoesNotExist:
        return None


def create_user(user_id, social_id):
    return User.create(social_id=social_id, username=user_id, role='user', is_active=True)


def get_or_create_user(facebook_data):
    user = get_user(facebook_data.data['id'])
    if user is None:
        return create_user(facebook_data.data['name'], facebook_data.data['id'])
    return user
