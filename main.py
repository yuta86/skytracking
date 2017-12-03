from app import app
from app import db
from calc.blueprint import calc

import api
import tasks
import view

app.register_blueprint(calc, url_prefix='/calc')



if __name__ == '__main__':  # Точка входа
    app.run(debug=True)

