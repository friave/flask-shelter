from ..models.animal import Animal, AnimalSchema
from flask import Blueprint, request, redirect
import json
from ..extensions import db

animals = Blueprint("animals", __name__)


@animals.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        animals_list = Animal.query.all()
        animals_schema = AnimalSchema(many=True)
        data = animals_schema.dump(animals_list)
        return json.dumps(data)


@animals.route('/available', methods=['POST'])
def add_animal():
    if request.method == "POST":
        data = request.json
        animal = Animal(name=data.get("name"), type=data.get("type"), desc=data.get("desc"), age=data.get("age"), adopted=data.get("adopted"))
        try:
            db.session.add(animal)
            db.session.commit()
            return json.dumps(AnimalSchema().dump(animal))
        except:
            return 'Issue adding animal'


@animals.route('/available', methods=['GET'])
def get_available_animals():
    if request.method == 'GET':
        animals_list = Animal.query.filter(Animal.adopted.is_(None))
        animals_schema = AnimalSchema(many=True)
        data = animals_schema.dump(animals_list)
        return json.dumps(data)


@animals.route('/adopted', methods=['GET'])
def get_adopted_animals():
    if request.method == 'GET':

        animals_list = Animal.query.filter(Animal.adopted.is_not(None))
        animals_schema = AnimalSchema(many=True)
        data = animals_schema.dump(animals_list)
        return json.dumps(data)

@animals.route('/<int:id>', methods=['GET'])
def get_animal(id):
    animal = Animal.query.get_or_404(id)
    if request.method == 'GET':
        return json.dumps(AnimalSchema().dump(animal))


def validate_put_request(data):
    if 'name' in data and 'age' in data and 'type' in data and 'desc' in data and 'adopted' in data:
        return True
    return False


@animals.route('/update/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    animal = Animal.query.get_or_404(id)
    data = request.json
    if request.method == 'PATCH':
        if (name := data.get('name')) is not None:
            animal.name = name
        if (age := data.get('age')) is not None:
            animal.age = age
        if (type := data.get('type')) is not None:
            animal.type = type
        if (desc := data.get('desc')) is not None:
            animal.desc = desc

        try:
            db.session.commit()
            return json.dumps(AnimalSchema().dump(animal))
        except:
            return 'Issue updating animal'

    if request.method == 'PUT':
        if validate_put_request(data):
            animal.name = data.get('name')
            animal.age = data.get('age')
            animal.type = data.get('type')
            animal.desc = data.get('desc')
            animal.adopted = data.get('adopted')

            try:
                db.session.commit()
                return json.dumps(AnimalSchema().dump(animal))
            except:
                return 'Issue updating animal'

        else:
            return "400, Invalid request: Some data is missing", 400


@animals.route('/<int:id>', methods=['DELETE'])
def delete(id):
    animal = Animal.query.get(id)

    try:
        db.session.delete(animal)
        db.session.commit()
        return 'Animal has been removed from animals list'
    except:
        return 'Issue deleting task'
