from flask import Blueprint
from project.models.user import User
from project.extensions import db

api = Blueprint('api', __name__)

@api.route('/user/<name>')
def get_user(name):
    user = User.query.filter_by(name="Mike").first()

    return {'user': user.name}
