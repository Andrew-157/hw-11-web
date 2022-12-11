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


@app.route('/address_book/phones/<int:user_id>', methods=['POST', 'DELETE'])
def add_phone(user_id):

    contact = Contact.query.filter_by(id=user_id).first()

    if not contact:

        return f"""<h1>Contact with ID {user_id} doesn't exist</h1>""", 404

    if request.method == 'POST':

        phone = request.json['phone']

        if Phone.query.filter_by(phone=phone).first():

            return f"""<h1>This phone number already exists in your Address Book<h1>"""

        check_phone = re.search(
            r"\([0-9]{2}\)\-[0-9]{3}\-[0-9]{1}\-[0-9]{3}|\([0-9]{2}\)\-[0-9]{3}\-[0-9]{2}\-[0-9]{2}", phone)

        if not check_phone:

            return f"""<h1>Phone should be of these formats: (00)-000-0-000 or (00)-000-00-00</h1>"""

        new_phone = Phone(contact_id=user_id, phone=phone)
        db.session.add(new_phone)
        db.session.commit()

        return f"""<h1>Phone number: {new_phone.phone} was added to contact {contact.name}<h1>"""

    if request.method == 'DELETE':

        phones = Phone.query.filter_by(contact_id=user_id).all()

        for value in phones:
            db.session.delete(value)
            db.session.commit()

        return f"""<h1>Phone numbers for {contact.name} were deleted</h1>"""
