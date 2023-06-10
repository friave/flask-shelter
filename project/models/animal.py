from sqlalchemy.orm import relationship

from .user import User
from ..extensions import db


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    adopted = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'desc': self.desc,
            'age': self.age,
        }