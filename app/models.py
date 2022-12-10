from . import db


class Contact(db.Model):

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)


class Phone(db.Model):

    __tablename__ = 'phones'

    contact_id = db.Column(db.Integer, db.ForeignKey(
        'contacts.id', ondelete="CASCADE", onupdate="CASCADE"))
    phone = db.Column(db.String(15), primary_key=True)
