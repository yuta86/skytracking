from wtforms import Form, StringField


class CalcForm(Form):
    param_a = StringField('Параметр А')
    param_b = StringField('Параметр В')
    operation = StringField('Операция')
