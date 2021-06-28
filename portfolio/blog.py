from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from portfolio.auth import login_required
from portfolio.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/blog')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.slug, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    print(tuple(posts[0]), "THIS SHOULDN'T BE A NUMBER")
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        db = get_db()
        title = request.form['title']
        body = request.form['body']
        error = None
        slug = ''.join(char for char in title if char.isalnum()).lower()[0:16]

        # We're using a cursor, so we can set the output to be just the list of results,
        # instead of a list of Row tuples. Otherwise we'd have to unpack them somehow
        cur = db.cursor()
        cur.row_factory = lambda cursor, row: row[0] 
        otherslugs = cur.execute( 'SELECT slug FROM post' ).fetchall()

        print(otherslugs[0][0])

        if slug in otherslugs:
            error = "Conflicting title."

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO post (slug, title, body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (slug, title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(slug, check_author=True):
    post = get_db().execute(
        'SELECT p.slug, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.slug = ?',
        (slug,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
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
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE slug = ?',
                (title, body, slug)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<slug>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(slug)
    db = get_db()
    db.execute('DELETE FROM post WHERE slug = ?', (slug,))
    db.commit()
    return redirect(url_for('blog.index'))