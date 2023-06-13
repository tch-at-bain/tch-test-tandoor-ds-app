from flask import Flask
from flask_session import Session
from utils import protected_route, protect_dash_views
from azure_ad import app_config


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(app_config)
    Session(app)

    with app.app_context():
        import routes
        from dash_app import init_dash_app

        app = init_dash_app(app)
        app = protect_dash_views(app)

        return app
