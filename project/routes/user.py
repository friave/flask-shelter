import json

from flask import Blueprint, request

from ..models.animal import Animal, AnimalSchema
from ..models.user import User, UserSchema
from ..extensions import db

users = Blueprint('user', __name__)


@users.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        data = request.json
        new_user = User(name=data.get("name"), surname=data.get("surname"))

        user_schema = UserSchema()
        data = user_schema.dump(new_user)
        try:
            db.session.add(new_user)
            db.session.commit()
            return json.dumps(data)
        except:
            return 'Issue adding animal'

    else:
        users = User.query.all()
        return json.dumps(UserSchema(many=True).dump(users))

@users.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'GET':
        return json.dumps(UserSchema().dump(user))


def validate_put_request(data):
    if 'name' in data and 'surname' in data:
        return True
    return False


@users.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    if request.method == 'PATCH':
        if (name := data.get('name')) is not None:
            user.name = name
        if (surname := data.get('surname')) is not None:
            user.surname = surname

        try:
            db.session.commit()
            return json.dumps(AnimalSchema().dump(user))
        except:
            return 'Issue updating user'

    if request.method == 'PUT':
        if validate_put_request(data):
            user.name = data.get('name')
            user.surname = data.get('surname')

            try:
                db.session.commit()
                return json.dumps(AnimalSchema().dump(user))
            except:
                return 'Issue updating user'

        else:
            return "400, Invalid request: Some data is missing", 400


@users.route('/<int:id>', methods=['DELETE'])
def delete(id):
    user = User.query.get(id)

    try:
        db.session.delete(user)
        db.session.commit()
        return 'User has been removed from users list'
    except:
        return 'Issue deleting task'


@users.route('/add_animal/<int:id>', methods=['PUT', 'PATCH'])
def add_animal(id):
    user = User.query.get_or_404(id)
    data = request.json
    animal = Animal.query.get(data.get('animal_id'))
    animal.adopted = user.id
    user.animals.append(animal)

    try:
        db.session.commit()
        return json.dumps(UserSchema().dump(user))
    except:
        return 'Issue adding animal to user'


@users.route('/<int:id>/adoptions', methods=['GET'])
def get_adopted_animals(id):
    if request.method == 'GET':
        animals = Animal.query.filter_by(adopted=id)
        animals_schema = AnimalSchema(many=True)
        data = animals_schema.dump(animals)
        return json.dumps(data)

@users.route('/<int:id>/adoptions/<int:id2>', methods=['GET'])
def get_adopted_animal(id, id2):
    if request.method == 'GET':
        animals = Animal.query.filter_by(adopted=id)

        for animal in animals:
            if animal.id == id2:
                animals_schema = AnimalSchema()
                data = animals_schema.dump(animal)
                return json.dumps(data)

        return "This user doesn't have this animal"

