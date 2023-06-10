from flask import Blueprint
from ..models.user import User
from ..extensions import db

main = Blueprint('main', __name__)

@main.route('/create_user/<name>')
def create_user(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()

    return "Created user"