from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from portfolio.auth import login_required
from portfolio.models import User, Post

bp = Blueprint('blog', __name__)

@bp.route('/blog')
def index():
    posts = Post.select(Post, User).join(User).order_by(Post.created.desc())
    print(posts)
    return render_template('blog/index.html', posts=posts)

''' TODO: Make this work
@bp.route('/blog/<slug>')
def post(slug):

    return
'''

# The login_required decorator is defined in auth.py
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        # The slug is the first 17 alphanumeric characters from the title, all lowercase
        # TODO: Put in the form! Let people change it
        slug = ''.join(char for char in title if char.isalnum()).lower()[0:16]

        if not title:
            error = 'Title is required.'

        if Post.get_or_none(Post.slug == slug) is not None:
            error = "Conflicting title."

        if error is not None:
            flash(error)
        else: # TODO! Make path work
            Post.create(slug=slug, title=title, blurb=body, path=title, author_id=g.user.user_id)
            return redirect(url_for('blog'))

    return render_template('blog/create.html')

def get_post(slug, check_author=True):
    post = Post.get_or_none(Post.slug == slug)

    if post is None:
        abort(404, f"Post named {slug} doesn't exist.")

    if check_author and post.author_id.user_id != g.user.user_id:
        abort(403)

    return post

@bp.route('/<slug>/update', methods=('GET', 'POST'))
@login_required
def update(slug):
    post = get_post(slug)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.blurb = body
            post.save()

            return redirect(url_for('blog'))

    return render_template('blog/update.html', post=post)

@bp.route('/<slug>/delete', methods=('POST',))
@login_required
def delete(slug):
    post =get_post(slug)
    post.delete_instance()

    return redirect(url_for('blog'))