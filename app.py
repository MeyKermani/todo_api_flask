from flask import Flask
from todo import views as todo_views
from users import views as users_views
from extensions import db, jwt, migrate
import manage


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("api")
    app.config.from_object("config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)
    configure_cli(app)

    return app


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(users_views.blueprint)
    app.register_blueprint(todo_views.blueprint)