import os
from flask import Flask, render_template, send_from_directory, request, g, escape

def create_app(test_config=None):

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'folio.sqlite'),
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

    @app.route("/character")
    def character():
        return render_template('character.html', title="About Us", url=os.getenv("URL"))


    @app.route("/health")
    def health():
        return "ok"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/blog', endpoint='index')

    return app