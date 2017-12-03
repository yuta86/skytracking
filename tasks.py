import flask
import json
from celery import Celery
from flask import request
from flask import Response
from app import api
from app import app
from app import db


from models import Calculate
from datetime import date, timedelta

from calc.blueprint import compute

app_celery = Celery('tasks', broker='amqp://localhost//', backend='db+mysql://root:root@localhost/celery_log')


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )



@app_celery.task(name='tasks.get_calc_all', bind=True)
@app.route('/my_api/v1.0/Calcall', methods=['GET'])
def get_calc_all():
    calcs = Calculate.query.order_by(Calculate.created.desc())
    temp_calcs = []

    for calc in calcs:
        temp_c = {"id": calc.id, "param_a": calc.param_a, "param_b": calc.param_b, "operation": calc.operation,
                  "result": calc.result,
                  "created": str(calc.created), "status": calc.status}
        temp_calcs.append(temp_c)

    return resp(200, {"temp_calcs": temp_calcs})


@app_celery.task(name='tasks.get_calc_sum', bind=True)
@app.route('/my_api/v1.0/Calc_sum', methods=['GET'])
def get_calc_sum():
    count_addition = 0  # 1
    count_subtraction = 0  # 2
    count_multiplication = 0  # 3
    count_division = 0  # 4
    count_exponentiation = 0  # 5

    yesterday = date.today() - timedelta(1)

    calcs = Calculate.query.filter(Calculate.created.contains(str(yesterday))).all()
    for calc in calcs:
        if calc.operation == 1:  # +
            count_addition = count_addition + 1
        elif calc.operation == 2:  # -

            count_subtraction = count_subtraction + 1
        elif calc.operation == 3:  # *

            count_multiplication = count_multiplication + 1
        elif calc.operation == 4:  # /

            count_division = count_division + 1
        elif calc.operation == 5:  # ^
            count_exponentiation = count_exponentiation + 1

    temp_c = {"addition": count_addition, "subtraction": count_subtraction, "multiplication": count_multiplication,
              "division": count_division,
              "exponentiation": count_exponentiation}

    return resp(200, {"GET LAST DAY": temp_c})


@app_celery.task(name='tasks.get_calc_operation', bind=True)
@app.route('/my_api/v1.0/get_calc_operation/<param_a>/<param_b>/<operation>', methods=['POST'])
def get_calc_operation(param_a, param_b=0, operation=0):
    jcalc = {}
    try:
        param_a = float(param_a)
        param_b = float(param_b)
        operation = int(operation)
        print('param_a = ' + str(param_a))
        print('param_b = ' + str(param_b))
        print('operation = ' + str(operation))
        temp_result = compute(param_a, param_b, operation)
        result = temp_result.get('result')

        status = str(temp_result.get('status'))
        remote_addr = str(request.remote_addr)
        user_agent = str(request.headers.get('User-Agent'))

        calc = Calculate(param_a=param_a, param_b=param_b, operation=operation, result=result, status=status,
                         remote_addr=remote_addr, user_agent=user_agent)
        session.add(calc)
        db.session.commit()
        jcalc = {"result": result}
    except:
        print("ERROR in create_calc")
    return resp(200, {"get_calc_operation:": jcalc})


# @app.route('/process/<name>')
# def process(name):
#     reverse.delay(name)
#     return 'hello '
#
# @app_celery.task(name='tasks.reverse')
# def reverse(string):
#     return string[::-1]

    #
    #
    # @app.route('/process/<name>')
    # def process(name):
    #     reverse.delay(name)
    #     return 'hello '

    #
    #
    # @app_celery.task(name='tasks.reverse')
    # def reverse(string):
    #     return string[::-1]


    # python -m celery -A tasks worker --loglevel=info Запуск задачи
    # python -m celery -A tasks.app_celery worker --loglevel=info Запуск задачи
