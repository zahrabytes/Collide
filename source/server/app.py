import os
from flask import Flask, jsonify
from suggest import retrieve_like_ids, retrieve_dislike_ids  # Importing from suggest.py
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import numpy as np
import openai

# Load environment variables
load_dotenv('../../.env.local')

# Initialize Flask app
app = Flask(__name__)

# Qdrant and OpenAI API keys and URLs from environment variables
QDRANT_API_KEY = os.getenv('Q_KEY')
QDRANT_URL = os.getenv('Q_URL')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')

# Initialize Qdrant client with API key
try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print("Successfully connected to Qdrant!")
except Exception as e:
    print(f"Error connecting to Qdrant: {str(e)}")

# OpenAI initialization
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# 1. Home route to test server is running
@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running'}), 200

# 2. API to get user by ID from Qdrant
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        result = client.retrieve(collection_name="collected_user_data", ids=[user_id])
        if result:
            return jsonify(result[0].payload), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. API to get recommended posts for a user using suggest.py
@app.route('/user/<int:user_id>/recommended_posts', methods=['GET'])
def get_recommended_posts(user_id):
    try:
        # Retrieve likes and dislikes from suggest.py
        likes = retrieve_like_ids(user_id, 3000)
        dislikes = retrieve_dislike_ids(user_id, 100)
        exclude_posts = likes + dislikes  # Combine liked and disliked posts for exclusion

        # Retrieve user's vectors from Qdrant
        result = client.retrieve(
            collection_name="collected_user_data",
            ids=[user_id],
            with_payload=True,
            with_vectors=True
        )

        if result:
            point = result[0]

            vector_dimension = 384  # Assuming your vectors have 384 dimensions
            default_vector = [0.0] * vector_dimension

            # Safely retrieve vectors or fallback to default_vector if missing
            posts_vector = np.array(point.vector.get('posts_vector', default_vector) or default_vector)
            comments_vector = np.array(point.vector.get('comments_vector', default_vector) or default_vector)
            likes_vector = np.array(point.vector.get('likes_vector', default_vector) or default_vector)
            dislikes_vector = np.array(point.vector.get('dislikes_vector', default_vector) or default_vector)

            # Combine embeddings with specific weights
            combined_embedding = (
                0.4 * posts_vector +
                0.3 * comments_vector +
                0.2 * likes_vector -
                0.1 * dislikes_vector
            )

            # Perform semantic search using the combined_embedding
            search_result = client.search(
                collection_name="posts",
                query_vector=combined_embedding.tolist(),
                limit=20,
                query_filter={
                    "must_not": [
                        # Exclude posts based on IDs from likes and dislikes
                        *[
                            {"key": "id", "match": {"value": post_id}} for post_id in exclude_posts
                        ],
                        # Exclude posts authored by the user
                        {"key": "authorable_id", "match": {"value": user_id}}
                    ]
                }
            )

            # Format the search results
            results = [
                {
                    'id': scored_point.id,
                    'score': scored_point.score,
                    'payload': scored_point.payload
                } for scored_point in search_result
            ]

            return jsonify({
                'user_id': user_id,
                'recommended_posts': results
            }), 200
        else:
            return jsonify({"error": "No data found for the user"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. API to get total number of users and classify them as active or inactive
@app.route('/users/stats', methods=['GET'])
def get_user_stats():
    try:
        # Retrieve all users from the "users" collection in Qdrant
        scroll_result = client.scroll(collection_name="users")
        all_users = scroll_result[0]  # Access the list of users
        total_users = len(all_users)

        # Example classification logic (modify based on actual data)
        active_users = [user for user in all_users if user.payload.get('last_active')]
        inactive_users = [user for user in all_users if not user.payload.get('last_active')]

        return jsonify({
            'total_users': total_users,
            'active_users': len(active_users),
            'inactive_users': len(inactive_users)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5. API to get all users' data (bio, location, etc.) from the "users" collection
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        scroll_result = client.scroll(collection_name="users")
        all_users = scroll_result[0]  # Access the list of users
        user_data = [user.payload for user in all_users]  # Extract payload data from each user

        return jsonify({'users': user_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 6. API to retrieve and summarize user collected data with OpenAI
# Helper function to split large text into smaller chunks
def split_text(text, max_len):
    return [text[i:i + max_len] for i in range(0, len(text), max_len)]

@app.route('/users/<int:user_id>/collected_data', methods=['GET'])
def get_user_collected_data(user_id):
    try:
        # Retrieve the collected data for a specific user from Qdrant
        collected_data_result = client.retrieve(
            collection_name="collected_user_data",
            ids=[user_id],
            with_payload=True,
            with_vectors=False
        )

        if not collected_data_result:
            return jsonify({"error": "User not found"}), 404

        # Extract data
        payload = collected_data_result[0].payload
        posts = payload.get('posts', '')

        # Split the posts into smaller chunks (1000 characters per chunk)
        post_chunks = split_text(posts, 1000)  # Adjust chunk size if needed

        summaries = []

        # Call OpenAI API for each chunk
        for chunk in post_chunks:
            prompt = f"Summarize this section: {chunk}"
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500  # Limit the token count of the response
            )
            # Collect summaries for each chunk
            summaries.append(response.choices[0].message.content)

        # Combine all the summaries into one
        final_summary = ' '.join(summaries)

        return jsonify({
            "collected_data": payload,
            "summary": final_summary
        }), 200

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
