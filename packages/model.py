from datetime import datetime
from extensions import db
from flask import Flask

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date_created = db.Column(db.DateTime,default=datetime.now)
    user_contact=db.relationship('Contact',backref='contact')

    def json(self):
        return {'id': self.id, 'name': self.name,
                'location': self.location, 'date_created': self.date_created}

    def get_user(_id):
        '''function to get movie using the id of the movie as parameter'''
        return [User.json(User.query.filter_by(id=_id).first())]


    def get_all_users():
        return [User.json(user) for user in User.query.all()]
   
    def update_movie(_id, _title, _year,):
        user_to_update = User.query.filter_by(id=_id).first()
        user_to_update.name = _title
        user_to_update.location = _year
        db.session.commit()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    p_num = db.Column(db.String(200))


    def json(self):
        return {'id': self.id, 'user_id': self.user_id,
                'p_num':self.p_num}


    def get_all_contacts():
        return [Contact.json(contact) for contact in Contact.query.all()]
    