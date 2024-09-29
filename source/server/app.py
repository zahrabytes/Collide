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

vector_dimension = 384
default_vector = [0.0] * vector_dimension

def retrieve_like_ids(user_id: int):
    likes_result = client.scroll(
        collection_name="likes",
        scroll_filter={
            "must": [
                {
                    "key": "authorable_id",
                    "match": {"value": user_id}
                }
            ]
        },
        limit=RECORDS_LIMIT,
        with_payload=True,
        with_vectors=False
    )
    user_likes_ids = [point.payload.get('likeable_id', '')for point in likes_result[0]]

    return user_likes_ids

def retrieve_dislike_ids(user_id: int):
    dislikes_result = client.scroll(
        collection_name="dislikes",
        scroll_filter={
            "must": [
                {
                    "key": "authorable_id",
                    "match": {"value": user_id}
                }
            ]
        },
        limit=RECORDS_LIMIT,
        with_payload=True,
        with_vectors=False
    )

    user_dislikes_ids = [point.payload.get('dislikeable_id', '')for point in dislikes_result[0]]

    return user_dislikes_ids

# API endpoint to check if the server is running
@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running'}), 200

@app.route('/users/posts/<int:user_id>', methods=['GET'])
def get_recommended_posts(user_id):

    likes = retrieve_like_ids(user_id)
    dislikes = retrieve_dislike_ids(user_id)

    exclude_posts = likes + dislikes

    try:
        # Retrieve a single point by ID
        result = client.retrieve(
            collection_name="collected_user_data",
            ids=[user_id],
            with_payload=True,
            with_vectors=True
        )
        
        if result:
            point = result[0]
            
            # Safely get vectors, using the default if a vector is missing or empty
            posts_vector = np.array(point.vector.get('posts_vector', default_vector) or default_vector)
            comments_vector = np.array(point.vector.get('comments_vector', default_vector) or default_vector)
            likes_vector = np.array(point.vector.get('likes_vector', default_vector) or default_vector)
            dislikes_vector = np.array(point.vector.get('dislikes_vector', default_vector) or default_vector)
            
            # Combine embeddings
            combined_embedding = (
                0.4 * posts_vector +
                0.3 * comments_vector +
                0.2 * likes_vector -
                0.1 * dislikes_vector
            )
            
            # Do semantic search against the posts collection
            search_result = client.search(
                collection_name="posts",
                query_vector=combined_embedding,
                limit=20,
                query_filter={
                    "must_not": [
                        # Exclude posts with IDs from likes and dislikes
                        *[
                            {
                                "key": "id",
                                "match": {
                                    "value": post_id
                                }
                            } for post_id in exclude_posts
                        ],
                        
                        # Exclude posts authored by the user
                        {
                            "key": "authorable_id",  
                            "match": {
                                "value": user_id  # Exclude user's own posts
                            }
                        }
                    ]
                }
            )
            
            results = [{
                'id': scored_point.id,
                'score': scored_point.score,
                'payload': scored_point.payload
            } for scored_point in search_result]
            
            return jsonify({'results': results})

        else:
            return jsonify({"error": f"Data not found for user {user_id}"}), 404
            
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
