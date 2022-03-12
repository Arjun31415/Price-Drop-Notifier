import json

from flask import Blueprint, redirect, render_template, request, url_for

from models.store import Store
from models.user import requires_admin, requires_login

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
@requires_login
def index():
    stores = Store.all()
    return render_template('stores/index.html', stores=stores)


@store_blueprint.route('/new', methods=['GET', 'POST'])
@requires_admin
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = None
        regex_query = None
        if request.form['query'] is not None:
            print("form query: ", request.form['query'])
            query = json.loads(request.form['query'])
        if request.form['regex-query'] is not None:
            regex_query = json.loads(request.form['regex-query'])
        Store(name, url_prefix, tag_name, query, regex_query=regex_query).save_to_db()
    return render_template('stores/new_store.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        form_query = request.form['query']
        form_query.replace("'", '"')
        print(form_query)
        query = json.loads(form_query)
        regex_query = json.loads(request.form['regex-query'])
        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query
        store.regex_query = regex_query
        store.save_to_db()
        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_db()
    return redirect(url_for('.index'))
