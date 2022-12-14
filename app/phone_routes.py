from flask import current_app as app
from flask import request
from app.models import Contact, Phone, db
import re


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


@app.route('/address_book/phones', methods=['PATCH'])
def change_phone():

    old_phone = request.args.get('phone')
    new_phone = request.json['phone']

    real_phone = Phone.query.filter(Phone.phone == old_phone).first_or_404()
    contact = Contact.query.filter_by(id=real_phone.contact_id).first()

    check_phone = re.search(
        r"\([0-9]{2}\)\-[0-9]{3}\-[0-9]{1}\-[0-9]{3}|\([0-9]{2}\)\-[0-9]{3}\-[0-9]{2}\-[0-9]{2}", new_phone)

    if not check_phone:
        f"""<h1>Phone should be of these formats: (00)-000-0-000 or (00)-000-00-00</h1>"""

    db.session.query(Phone).filter_by(
        phone=old_phone).update({'phone': new_phone})
    db.session.commit()

    return f"""<h1>{old_phone} was changed to {new_phone} for contact {contact.name}</h1>"""
