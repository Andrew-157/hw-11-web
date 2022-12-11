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
def edit_phone(user_id):

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


@app.route('/address_book/phones', methods=['DELETE'])
def delete_phone():

    phone = request.args.get('phone')

    real_phone = Phone.query.filter(Phone.phone == phone).first_or_404()

    contact = Contact.query.filter(Contact.id == real_phone.contact_id).first()

    db.session.delete(real_phone)
    db.session.commit()

    return f"""<h1>Phone number {real_phone.phone} was deleted for contact {contact.name}</h1>"""


@app.route('/address_book/contacts/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_contact(user_id):

    contact = Contact.query.filter_by(id=user_id).first_or_404()

    if request.method == 'DELETE':

        contact = Contact.query.filter(Contact.id == user_id).first()
        db.session.delete(contact)
        db.session.commit()

        return f"""<h1>User {contact.name} was deleted</h1>"""

    if request.method == 'PUT':

        name = request.json['name']
        email = request.json['email']

        check_email = re.search(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email)

        if not check_email:
            old_name = contact.name
            db.session.query(Contact).filter_by(
                id=user_id).update({'name': name})
            db.session.commit()
            return f"""<h1>Contact {old_name} was changed to {name}, but {email} is of the wrong format</h1>"""

        old_name = contact.name
        old_email = contact.email
        db.session.query(Contact).filter_by(
            id=user_id).update({'name': name, 'email': email})
        db.session.commit()
        return f"""<h1>Contact {old_name} was changed to {name}, {old_email if not old_email else "NO EMAIL"} was changed to {email}</h1>"""

    phone_values = []
    for value in Phone.query.filter_by(contact_id=user_id).all():
        phone_values.append(value.phone)

    return f"""<h1>Contact name: {contact.name},\nContact email: {"No email" if not contact.email else contact.email},\nContact phones: {phone_values}</h1>"""


@app.route('/address_book/contacts', methods=['GET'])
def get_contact():

    name = request.args.get('name')
    email = request.args.get('email')
    phone = request.args.get('phone')
    phone_values = []

    if name:

        contact = Contact.query.filter(Contact.name == name).first_or_404()
        for value in Phone.query.filter_by(contact_id=contact.id).all():
            phone_values.append(value.phone)

    if email:

        contact = Contact.query.filter(Contact.email == email).first_or_404()
        for value in Phone.query.filter_by(contact_id=contact.id).all():
            phone_values.append(value.phone)

    if phone:

        real_phone = Phone.query.filter(Phone.phone == phone).first_or_404()

        contact = Contact.query.filter(
            Contact.id == real_phone.contact_id).first()

        for value in Phone.query.filter_by(phone=real_phone.phone).all():
            phone_values.append(value.phone)

    return f"""<h1>Contact name: {contact.name},\nContact email: {"No email" if not contact.email else contact.email},\nContact phones: {phone_values}</h1>"""
