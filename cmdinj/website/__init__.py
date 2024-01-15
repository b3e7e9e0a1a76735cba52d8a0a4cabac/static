from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'VERY_SECRET_KEY'

    from .vuln import vuln

    app.register_blueprint(vuln, url_prefix='/')
    return app

