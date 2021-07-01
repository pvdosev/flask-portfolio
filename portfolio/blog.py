from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from portfolio.auth import login_required
from portfolio.models import User, Post

bp = Blueprint('blog', __name__)

@bp.route('/blog')
def index():
    #db = get_db()
    posts = Post.select(Post, User).join(User).order_by(Post.created.desc())
    print(posts)
    #db.execute('SELECT p.slug, title, body, created, author_id, username'' FROM post p JOIN user u ON p.author_id = u.id'' ORDER BY created DESC').fetchall()
    return render_template('blog/index.html', posts=posts)

''' TODO: Make this work
@bp.route('/blog/<slug>')
def post(slug):
    db = get_db()
    post = db.execute(
        'SELECT p.slug, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.slug = ?',
        (slug)
    ).fetchone()

    return post
'''

# The login_required decorator is defined in auth.py
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        #db = get_db()
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
            '''db.execute(
                'INSERT INTO post (slug, title, body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (slug, title, body, g.user['id'])
            )
            db.commit()'''
            return redirect(url_for('blog'))

    return render_template('blog/create.html')

def get_post(slug, check_author=True):
    post = get_or_none(Post.slug == slug)
    '''get_db().execute(
        'SELECT p.slug, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.slug = ?',
        (slug)
    ).fetchone()'''

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user.id:
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
            #db = get_db()
            '''db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE slug = ?',
                (title, body, slug)
            )
            db.commit()'''
            return redirect(url_for('blog'))

    return render_template('blog/update.html', post=post)

@bp.route('/<slug>/delete', methods=('POST',))
@login_required
def delete(slug):
    post =get_post(slug)
    post.delete_instance()
    #db = get_db()
    #db.execute('DELETE FROM post WHERE slug = ?', (slug,))
    #db.commit()
    return redirect(url_for('blog'))