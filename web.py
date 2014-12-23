from flask import Flask, render_template, request, redirect, url_for
import db_mods
import utils
app = Flask(__name__)

@app.route('/<int:number_of_posts>/', methods='get')
@app.route('/')
def main(number_of_posts=10):
    posts = utils.sort_by_rank(db_mods.ranked_post_details(number_of_posts))
    return render_template('posts.html', posts=posts)

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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'