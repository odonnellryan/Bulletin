from flask import Flask, render_template, request, redirect, url_for, session, g
import db_mods
import utils
import config
app = Flask(__name__)


@app.route('/', defaults={'page':1})
@app.route('/<int:page>/')
def main(page):
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

@app.route('/update/<int:pk>', methods='get')
def update(pk=None):
    post = db_mods.find_post(pk)
    return render_template('update.html', post=post)

@app.route('/delete/<int:pk>', methods='get')
def delete(pk=None):
    post = db_mods.find_post(pk)
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