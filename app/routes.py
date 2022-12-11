from flask import current_app as app
from flask import request
from app.models import Contact, Phone, db
import re


@app.route('/address_book/')
def welcome_func():
    return """
                <h1>Welcome to your Address Book</h1>"""


@app.route('/address_book/contacts', methods=['POST'])
def create_user():

    name = request.json['name']

    contact = Contact.query.filter(Contact.name == name).first()

    if contact:

        return f"""<h1>Contact {name} already exists</h1>""", 409

    if "email" in request.json:

        email = request.json["email"]

        check_email = re.search(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email)

        if not check_email:

            new_contact = Contact(name=name)
            db.session.add(new_contact)
            db.session.commit()

            return f"""<h1>Contact {name} was created, but his email is of the wrong format</h1>"""

        new_contact = Contact(name=name, email=email)
        db.session.add(new_contact)
        db.session.commit()

        return f"""Contact {name} with {email} was added"""

    new_contact = Contact(name=name)
    db.session.add(new_contact)
    db.session.commit()

    return f"""<h1>Contact {name} was created</h1>"""
