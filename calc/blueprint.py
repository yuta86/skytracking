from flask import Blueprint
from flask import render_template

from models import Calculate
from .forms import CalcForm
from flask import request
from app import db
from flask import redirect
from flask import url_for

calc = Blueprint('calc', __name__, template_folder='templates')


def compute(param_a, param_b, operation):
    """
    :param param_a: Первый параметр
    :param param_b: Второй параметр
    :param operation: Математическая операция
    :return: Результат математической операции как словарь с ключами result и status
    """
    result = {}
    temp = 0
    if operation == 1:  # +
        print('1')
        temp = param_a + param_b
        result['result'] = temp
        result['status'] = 'SUCCESSFUL execution of the function'
        print ('temp=' + str(temp))
    elif operation == 2:  # -
        print('2')
        temp = param_a - param_b
        result['result'] = temp
        result['status'] = 'SUCCESSFUL execution of the function'
    elif operation == 3:  # *
        print('3')
        temp = param_a * param_b
        result['result'] = temp
        result['status'] = 'SUCCESSFUL execution of the function'
    elif operation == 4:  # /
        print('4')
        if param_b != 0:
            temp = param_a / param_b
            result['result'] = temp
            result['status'] = 'SUCCESSFUL execution of the function'
        else:
            print('delenie na 0 !!!')
            result['result'] = 0
            result['status'] = 'ERROR, can not divide by zero'
    elif operation == 5:  # ^
        print('5')
        temp = param_a ** param_b
        result['result'] = temp
        result['status'] = 'SUCCESSFUL execution of the function'
    else:
        print('error!!!!!!')
        result['result'] = 0
        result['status'] = 'ERROR, unknown operation'

    return result


@calc.route('/create', methods=['POST', 'GET'])
def create_calc():
    if request.method == "POST":
        print (request.remote_addr)
        print (request.headers.get('User-Agent'))
        remote_addr = str(request.remote_addr)
        user_agent = str(request.headers.get('User-Agent'))

        try:
            param_a = float(request.form['param_a'])
            param_b = float(request.form['param_b'])
            operation = int(request.form['operation'])
            # print('param_a = ' + str(param_a))
            # print('param_b = ' + str(param_b))
            # print('operation = ' + str(operation))
            temp_result = compute(param_a, param_b, operation)
            result = temp_result.get('result')

            status = str(temp_result.get('status'))


            calc = Calculate(param_a=param_a, param_b=param_b, operation=operation, result=result, status=status,
                             remote_addr=remote_addr, user_agent=user_agent)
            db.session.add(calc)
            db.session.commit()
        except:
            print("ERROR in create_calc")

        return redirect(url_for('calc.index'))
    print('get--------')
    form = CalcForm()
    return render_template('calc/create_calc.html', form=form)


@calc.route('/')
def index():
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    calcs = Calculate.query.order_by(Calculate.created.desc())

    pages = calcs.paginate(page=page, per_page=5)

    return render_template('calc/index.html', calcs=calcs, pages=pages)


@calc.route('/<id>')
def calc_detail(id):
    calc = Calculate.query.filter(Calculate.id == id).first_or_404()
    return render_template('calc/calc_detail.html', calc=calc)
