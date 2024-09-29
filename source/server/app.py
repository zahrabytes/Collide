import os
import openai
import numpy as np
from flask import Flask, jsonify
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv('..//.env.local')

# Qdrant API key from environment variables
QDRANT_API_KEY = os.getenv('Q_KEY')
QDRANT_URL = os.getenv('Q_URL')
OPENAI_KEY = os.getenv('OPENAI_KEY')

openai.api_key=OPENAI_KEY

# Initialize Qdrant client with API key
client = QdrantClient(
    url=QDRANT_URL, 
    api_key=QDRANT_API_KEY
)

RECORDS_LIMIT=5000

# API endpoint to check if the server is running
@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running'}), 200

@app.route('/trendingtopics', methods=['GET'])
def get_trendingtopics():
    try:
        collected_post_result = client.scroll(
            collection_name="posts",
            with_payload=True,
            with_vectors=False
        )

        if not collected_post_result or len(collected_post_result) == 0:
            return jsonify({"error": "posts not found"}), 404
        
        collected_comment_result = client.scroll(
            collection_name="comments",
            with_payload=True,
            with_vectors=False
        )

        if not collected_post_result or len(collected_comment_result) == 0:
            return jsonify({"error": "comments not found"}), 404

        # Rest of OpenAI code...
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"This is collected data from a userbase. Give me a list of 20 trending topics (they must be quality topics, not just frequently mentioned words, two words each, in list separated by commas, without summarry): {collected_post_result} {collected_comment_result}",
            }],
        )
        return jsonify(response.choices[0].message.content), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/count', methods=['GET'])
def get_user_count():
    try:
        collection_info = client.get_collection("collected_user_data")
        total_users = collection_info.points_count

        return jsonify({'total_users': total_users})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users_result = client.scroll(
            collection_name="users",
            limit=RECORDS_LIMIT,
            with_payload=True,
            with_vectors=False
        )

        # If no result is found, return 404
        if not users_result or len(users_result) == 0:
            return jsonify({"error": "Users not found"}), 404
        
        # Extract user data from the collected_data_result
        users_data = [user.payload for user in users_result[0]]

        # Return the user data as a JSON response
        return jsonify(users_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API endpoint to get user data by user ID from the Qdrant collection
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Retrieve user data from Qdrant using the user ID
        collected_data_result = client.retrieve(
            collection_name="collected_user_data",
            ids=[user_id],
            with_payload=True,
            with_vectors=False
        )
        
        # If no result is found, return 404
        if not collected_data_result or len(collected_data_result) == 0:
            return jsonify({"error": "User not found"}), 404
        
        # Extract user data from the collected_data_result
        user_data = collected_data_result[0].payload

        # Pass user data to OpenAI 
        openai_prompt = f"This is collected data from a user. Make me a summary about them {user_data}"

        # Rest of OpenAI code...
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": openai_prompt,
            }],
        )

        # Return the user data as a JSON response
        return jsonify(response.choices[0].message.content), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
