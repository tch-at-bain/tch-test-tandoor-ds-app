from functools import wraps
from flask import session, redirect, url_for
from azure_ad import app_config
import yaml


def get_config():
    with open("src/config/config.yaml") as fp:
        return yaml.safe_load(fp)


def protected_route(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        config = get_config()
        sso_enabled = config["auth"]["sso"]["enabled"]

        if not session.get("user") and sso_enabled:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapped_function


def protect_dash_views(app):
    for view_func in app.server.view_functions:
        if view_func.startswith(app_config.DASH_ROUTE_PATHNAME):
            app.server.view_functions[view_func] = protected_route(
                app.server.view_functions[view_func]
            )
    return app
