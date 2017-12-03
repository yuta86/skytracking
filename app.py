from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask.ext.restless import APIManager
# from celery import Celery

app = Flask(__name__)
app.config.from_object(Configuration)  # передача конфигурации

db = SQLAlchemy(app)

api = APIManager(app, flask_sqlalchemy_db=db)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# celery = Celery(app.name, broker='amqp://localhost//', backend='db+mysql://root:root@localhost/celery_log')

