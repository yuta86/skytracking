# from app import api
# # from tasks import app_celery
# from app import app
# from models import Calculate
# from app import db
# import json
# from flask import Response
# import flask
# from datetime import date, timedelta
# from celery import Celery
# from calc.blueprint import compute
# from flask import request
# from app import celery
#
#
# # app_celery = Celery('tasks', broker='amqp://localhost//', backend='db+mysql://root:root@localhost/celery_log')
#
# # api.create_api(Calculate, methods=['GET', 'POST'])  # http://127.0.0.1:5000/api/calculate
#
#
# # Моя реализация
#
# def to_json(data):
#     return json.dumps(data) + "\n"
#
#
# def resp(code, data):
#     return flask.Response(
#         status=code,
#         mimetype="application/json",
#         response=to_json(data)
#     )
#
#
#
