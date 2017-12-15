from flask import Flask, render_template, request, redirect, url_for, g
from flask_login import current_user, logout_user

import config
import db_mods
import utils

app = Flask(__name__)


@app.route('/', defaults={'page': 1})
@app.route('/<int:page>/')
def main(page):
    posts = utils.post_mods(db_mods.ranked_post_details(), current_user)
    g.pagination = utils.Pagination(config.page_length, posts, page)
    posts = g.pagination.posts_by_page
    pages = g.pagination.pages
    next_page = g.pagination.next_page
    prev_page = g.pagination.prev_page
    if page != 1 and page > pages:
        return redirect(url_for('main'))
    pages = range(1, pages + 1)
    return render_template('posts.html', posts=posts, pages=pages, next_page=next_page, prev_page=prev_page)


@app.route('/delete/<int:pk>/', methods=['get', 'post'])
def delete(pk=None):
    post = db_mods.find_post(pk)
    if request.method == 'POST' and post:
        db_mods.delete_post(pk)
        return redirect(url_for('main'))
    return render_template('delete.html', post=post)


@app.route('/new/', methods=['get', 'post'])
def new():
    if request.method == 'POST':
        if current_user.is_authenticated:
            db_mods.new_post(request.form['title'], request.form['content'], request.form['points'], current_user.pk)
        return redirect(url_for('main'))
    return render_template('new.html')


@app.route('/edit/<int:pk>/', methods=['get', 'put'])
def edit(pk=None):
    post = db_mods.find_post(pk)
    if request.method == 'PUT' and post:
        try:
            rank = int(request.form['rank'])
        except ValueError:
            # TODO: add errors/alerts here
            return redirect(url_for('main'))
        db_mods.edit_post(request.form['title'], request.form['content'], request.form['points'], current_user.pk)
        return redirect(url_for('main'))
    return render_template('edit.html', post=post)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main'))
