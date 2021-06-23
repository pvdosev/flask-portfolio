import os
from flask import Flask, render_template, send_from_directory, request, g, escape

from app.python.database import Database

def create_app(test_config=None):

    app = Flask(__name__)

    UPLOAD_FOLDER = '../app/static/img'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    databaseHolder = Database()

     app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html', title="Gamer Fellowship", url=os.getenv("URL"))

    @app.route('/blog')
    def blog():
        return "hi"

    @app.route('/blog/<post>')
    def post(post):
         return f"Hello, {escape(post)}!"

    @app.route("/character")
    def character():
        return render_template('character.html', title="About Us", url=os.getenv("URL"))


    @app.route("/health")
    def health():
        return "ok"

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    return app