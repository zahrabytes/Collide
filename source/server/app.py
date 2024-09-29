import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Qdrant API key from environment variables
QDRANT_API_KEY = os.getenv('Q_KEY')
QDRANT_URL = os.getenv('Q_URL')

# Initialize Qdrant client with API key
client = QdrantClient(
    url=QDRANT_URL, 
    api_key=QDRANT_API_KEY
)

# API endpoint to check if the server is running
@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running'}), 200

# API endpoint to get user data by user ID from the Qdrant collection
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Retrieve user data from Qdrant using the user ID
        result = client.retrieve(
            collection_name="users",  # Assuming the collection name is 'users'
            ids=[user_id]
        )
        
        # If no result is found, return 404
        if not result or len(result) == 0:
            return jsonify({"error": "User not found"}), 404
        
        # Extract user data from the result
        user_data = result[0].payload
        
        # Return the user data as a JSON response
        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
