import os
from datetime import datetime

import click
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
        password: Mapped[str] = mapped_column(String, unique=True, nullable=False)

class Post(db.Model):
        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True, nullable=False)
        title: Mapped[str] = mapped_column(String, nullable=False)
        body: Mapped[str] = mapped_column(String, nullable=False)
        created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

@click.command('init-db')
def init_db_command():

        global db
        with current_app.app_context():
                db.create_all()
        click.echo("Initialized the database!")


def create_app(test_config=None):

        app = Flask(__name__, instance_relative_config=True)
        app.config.from_mapping(
                SECRET_KEY='dev',
                SQLALCHEMY_DATABASE_URI='sqlite:///database.sqlite'
        )

        if test_config is None:
                app.config.from_pyfile('config.py', silent=True)
        else:
                app.config.from_mapping(test_config)

        try:
                os.mkdir(app.instance_path)
        except OSError:
                pass

        app.cli.add_command(init_db_command)

        db.init_app(app)

        from src.controller import user

        app.register_blueprint(user.app)
        return app

