import json
import os

import jinja2
from flask import Flask, render_template

from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(64)
    app.config.update(
        ADMIN=os.environ.get('ADMIN')
    )
    jinja2.Environment(autoescape=True).filters['tojson'] = json.dumps

    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')

    app.register_blueprint(alert_blueprint, url_prefix="/alerts")
    app.register_blueprint(store_blueprint, url_prefix="/stores")
    app.register_blueprint(user_blueprint, url_prefix="/users")

# if __name__ == '__main__':
#     app.run(debug=True)
