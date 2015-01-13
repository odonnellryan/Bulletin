from flask import Flask, render_template, request, redirect, url_for, session, g
import db_mods
import utils
import config
app = Flask(__name__)


@app.route('/', defaults={'page':1})
@app.route('/<int:page>/')
def main(page):
    # begin way to track if a user has already upvoted/downvoted
    # this is a no account app, but we still want it to track as best we can if we've voted.
    if page == 1:
        session_info = session.get('bulletin-rank-values') or None
        session['posts'] = utils.post_mods(db_mods.ranked_post_details(), session_info)
    g.pagination = utils.Pagination(config.page_length, session['posts'], page)
    posts = g.pagination.posts_by_page
    pages = g.pagination.pages
    next_page = g.pagination.next_page
    prev_page = g.pagination.prev_page
    if page > pages:
        return redirect(url_for('main'))
    pages = range(1, pages + 1)
    return render_template('posts.html', posts=posts, pages=pages, next_page=next_page, prev_page=prev_page)

@app.route('/delete/<int:pk>/', methods=['get','post'])
def delete(pk=None):
    post = db_mods.find_post(pk)
    if request.method == 'POST' and post:
        db_mods.delete_post(pk)
        return redirect(url_for('main'))
    return render_template('delete.html', post=post)

@app.route('/new/', methods=['get','post'])
def new():
    if request.method == 'POST':
        try:
            rank = int(request.form['rank'])
        except ValueError:
            rank = 0
        db_mods.new_post(request.form['title'], request.form['content'], rank)
        return redirect(url_for('main'))
    return render_template('new.html')

@app.route('/edit/<int:pk>/', methods=['get','put'])
def edit(pk=None):
    post = db_mods.find_post(pk)
    if request.method == 'PUT' and post:
        try:
            rank = int(request.form['rank'])
        except ValueError:
            # TODO: add errors/alerts here
            return redirect(url_for('main'))
        db_mods.update_post(pk, request.form['title'], request.form['content'], rank)
        return redirect(url_for('main'))
    return render_template('edit.html', post=post)