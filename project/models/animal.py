from ..extensions import db, ma


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    adopted = db.Column(db.Integer, db.ForeignKey("user.id"))


class AnimalSchema(ma.Schema):
    class Meta:
        model = Animal
        fields = ('id', 'name', 'type', 'desc', 'age', 'adopted')
        include_relationships = True
