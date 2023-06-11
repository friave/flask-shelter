from .animal import AnimalSchema
from ..extensions import db, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    animals = db.relationship('Animal', backref='user')

    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'surname': self.surname,
    #         'animals': self.animals
    #     }


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    animals = ma.Nested(AnimalSchema, many=True)
