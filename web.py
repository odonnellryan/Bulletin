from flask import Flask, render_template
import db_mods
import utils
app = Flask(__name__)

@app.route('/<int:number_of_posts>/', methods='get')
@app.route('/')
def main(number_of_posts=10):
    posts = db_mods.ranked_post_details(number_of_posts)
    return render_template('posts.html', posts=posts)

@app.route('/update/<int:id>', methods='get')
def update(id=None):
    post = db_mods.post_by_id(id)
    return render_template('update.html', post=post)

@app.route('/delete/<int:id>', methods='get')
def delete(id=None):
    post = db_mods.post_by_id(id)
    return render_template('delete.html', post=post)

@app.route('/new/', methods='get')
def new():
    return render_template('new.html')
