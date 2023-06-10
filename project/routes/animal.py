from ..models.animal import Animal
from flask import Blueprint, request, redirect
import json
from ..extensions import db

animal = Blueprint("animals", __name__)


@animal.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        data = request.json
        new_animal = Animal(name=data.get("name"), type=data.get("type"), desc=data.get("desc"), age=data.get("age"))

        try:
            db.session.add(new_animal)
            db.session.commit()
            return json.dumps(new_animal.serialize())
        except:
            return 'Issue adding animal'

    else:
        tasks = Animal.query.all()
        json_tasks = [e.serialize() for e in tasks]
        return json.dumps(json_tasks)


@animal.route('/<int:id>', methods=['GET'])
def get_animal(id):
    animal = Animal.query.get_or_404(id)
    if request.method == 'GET':
        return json.dumps(animal.serialize())


def validate_post_request(data):
    if ('name' in data and 'age' in data and 'type' in data and 'desc' in data):
        return True
    return False


@animal.route('/update/<int:id>', methods=['PUT', 'PATCH'])
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
            return json.dumps(animal.serialize())
        except:
            return 'Issue updating animal'

    if request.method == 'PUT':
        if validate_post_request(data):
            animal.name = data.get('name')
            animal.age = data.get('age')
            animal.type = data.get('type')
            animal.desc = data.get('desc')

            try:
                db.session.commit()
                return json.dumps(animal.serialize())
            except:
                return 'Issue updating animal'

        else:
            return "400, Invalid request: Some data is missing", 400


@animal.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    animal = Animal.query.get(id)

    try:
        db.session.delete(animal)
        db.session.commit()
        return 'Animal has been removed from animals list'
    except:
        return 'Issue deleting task'
