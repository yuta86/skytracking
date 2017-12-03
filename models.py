from app import db
from datetime import datetime

operations = (
    ('addition', '+'),  # 1
    ('subtraction', '-'),  # 2
    ('multiplication', '*'),  # 3
    ('division', '/'),  # 4
    ('exponentiation', '^'),  # 5
)


class Calculate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param_a = db.Column(db.Float)
    param_b = db.Column(db.Float)
    operation = db.Column(db.Integer)
    result = db.Column(db.Float)
    created = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(140))
    remote_addr = db.Column(db.String(15))  # 4*3+1*3
    user_agent = db.Column(db.String(140))

    # log = db.Column(db.Integer, db.ForeignKey('log.id'))

    def __init__(self, *args, **kwargs):
        super(Calculate, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Calculate id: {}, a: {}, b: {}, operation: {}, result: {} >'.format(self.id, self.param_a,
                                                                                     self.param_b, self.operation,
                                                                                     self.result)

# class Log(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     remote_addr = db.Column(db.String(15))  # 4*3+1*3
#     user_agent = db.Column(db.String(140))
#
#     def __init__(self, *args, **kwargs):
#         super(Log, self).__init__(*args, **kwargs)
#
#     def __repr__(self):
#         return '<Log id: {}, remote_addr: {} , user_agent: {} >'.format(self.id, self.remote_addr, self.user_agent)
