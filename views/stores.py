from flask import Blueprint, request, render_template, request, url_for
import json
from models.store import Store

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/index.html', stores=stores)


@store_blueprint.route('/new', methods=['GET', 'POST'])
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        Store(name, url_prefix, tag_name, query).save_to_db()
    return render_template('stores/new_store.html')
