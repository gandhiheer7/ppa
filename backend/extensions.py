from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from celery import Celery

cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()

def make_celery(app_name=__name__):
    return Celery(app_name, broker="redis://localhost:6379/1", backend="redis://localhost:6379/2")

celery_app = make_celery()