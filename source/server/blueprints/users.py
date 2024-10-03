from flask import Blueprint, jsonify
from services import UsersService

users = Blueprint('users', __name__, url_prefix='/users')
users_service = UsersService()

@users.route('/', methods=['GET'])
def get_all_users() -> dict:

    all_users = users_service.get_all_users()

    if all_users:

    	return jsonify({'users': [user.payload for user in all_users[0]]}), 200

    return jsonify({'error': 'Could not find users'}), 404




	








