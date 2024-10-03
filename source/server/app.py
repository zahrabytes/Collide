from flask import Flask
from flask_cors import CORS
from blueprints import user, users, trending_topics

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(users)
app.register_blueprint(trending_topics)
CORS(app)

@app.route('/', methods=['GET'])
def home():
	return jsonify({'message': 'Flask server is running'})

if __name__ == '__main__':
	app.run()

