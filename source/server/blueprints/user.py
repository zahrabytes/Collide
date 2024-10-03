from flask import Blueprint, jsonify
from services import UserService

user = Blueprint('user', __name__, url_prefix='/user')
user_service = UserService()

@user.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> dict:

	user = user_service.get_user(user_id)

	if user:
		return jsonify(user), 200

	return jsonify({'error': f'User with id {user_id} not found'}), 404

@user.route('/<int:user_id>/recommendedposts', methods=['GET'])
def get_recommended_posts(user_id: int) -> dict:

	recommended_posts = user_service.get_recommended_posts(user_id)

	if recommended_posts:
		return jsonify({'posts': recommended_posts}), 200

	return jsonify({'error': f'Data not found for user with id {user_id}'}), 404

@user.route('/<int:user_id>/recommendedusers', methods=['GET'])
def get_recommended_users(user_id: int) -> tuple:

	recommended_users = user_service.get_recommended_users(user_id)

	if recommended_users:
		return (recommended_users, 200)

	return jsonify({'error': f'Data not found for user with id {user_id}'}), 404

@user.route('/<int:user_id>/analytics/topicsmatch/<string:topics>', methods=['GET'])
def get_user_topics_match(user_id: int, topics: str) -> tuple:

	topics_match = user_service.get_user_topics_match(user_id, topics)

	if topics_match:
		return (topics_match, 200)

	return jsonify({'error': f'Could not get topics for user with id {user_id}'}), 404

@user.route('/<int:user_id>/analytics/interests', methods=['GET'])
def get_user_interests(user_id: int) -> tuple:

	interests = user_service.get_user_interests(user_id)

	if interests:
		return (interests, 200)

	return jsonify({'error': f'Could not get interests for user with id {user_id}'}), 404

@user.route('/<int:user_id>/summary', methods=['GET'])
def get_user_summary(user_id: int) -> tuple:

	user_summary = user_service.get_user_summary(user_id)

	if user_summary:
		return (user_summary, 200)

	return jsonify({'error': f'Could not get user summary for user with id {user_id}'})