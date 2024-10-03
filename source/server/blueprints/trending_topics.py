from flask import Blueprint, jsonify
from services import TrendingTopicsService

trending_topics = Blueprint('trending_topics', __name__, url_prefix='/trendingtopics')
trending_topics_service = TrendingTopicsService() 

@trending_topics.route('/', methods=['GET'])
def get_trending_topics() -> tuple:

	trending_topics = trending_topics_service.get_trending_topics()

	if trending_topics:
		return (trending_topics, 200)

	return jsonify({'error': 'There was an error getting the trending topics'}), 404

