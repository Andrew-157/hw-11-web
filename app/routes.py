from flask import current_app as app
from flask import request
from app.models import Contact, Phone, db


@app.route('/address_book/')
def welcome_func():
    return """
                <h1>Welcome to you Address Book<h1>"""


@app.route('/address_book/contacts', methods=['POST'])
def create_user():
    pass
