import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from extensions import db
    from models import User

    click.echo("create user")
    user = User(username="admin", email="meysamkermani@gmail.com", password="1234qwer")
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
