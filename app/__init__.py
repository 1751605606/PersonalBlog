from flask import Flask
from .my_sqlalchemy import MySQLAlchemy
from config import config
db = MySQLAlchemy()
# 蓝本需要db，所以蓝本要在db之后引入
from .blue_print import blue_print


def create_app(config_name):
    app = Flask(__name__)
    app.register_blueprint(blue_print)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    return app


