import os
import openai
import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import NamedVector
from qdrant_client.http import models

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv("..//.env.local")

# Qdrant API key from environment variables
QDRANT_API_KEY = os.getenv("Q_KEY")
QDRANT_URL = os.getenv("Q_URL")
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY

# Initialize Qdrant client with API key
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

RECORDS_LIMIT = 5000

vector_dimension = 384
default_vector = [0.0] * vector_dimension


def retrieve_like_ids(user_id: int):
    likes_result = client.scroll(
        collection_name="likes",
        scroll_filter={"must": [{"key": "authorable_id", "match": {"value": user_id}}]},
        limit=RECORDS_LIMIT,
        with_payload=True,
        with_vectors=False,
    )
    user_likes_ids = [point.payload.get("likeable_id", "") for point in likes_result[0]]

    return user_likes_ids


def retrieve_dislike_ids(user_id: int):
    dislikes_result = client.scroll(
        collection_name="dislikes",
        scroll_filter={"must": [{"key": "authorable_id", "match": {"value": user_id}}]},
        limit=RECORDS_LIMIT,
        with_payload=True,
        with_vectors=False,
    )

    user_dislikes_ids = [
        point.payload.get("dislikeable_id", "") for point in dislikes_result[0]
    ]

    return user_dislikes_ids


# API endpoint to check if the server is running
@app.route("/")
def home():
    return jsonify({"message": "Flask server is running"}), 200


@app.route("/users/<int:user_id>/recommendedposts", methods=["GET"])
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
            with_vectors=True,
        )

        if result:
            point = result[0]

            # Safely get vectors, using the default if a vector is missing or empty
            posts_vector = np.array(
                point.vector.get("posts_vector", default_vector) or default_vector
            )
            comments_vector = np.array(
                point.vector.get("comments_vector", default_vector) or default_vector
            )
            likes_vector = np.array(
                point.vector.get("likes_vector", default_vector) or default_vector
            )
            dislikes_vector = np.array(
                point.vector.get("dislikes_vector", default_vector) or default_vector
            )

            # Combine embeddings
            combined_embedding = (
                0.4 * posts_vector
                + 0.3 * comments_vector
                + 0.2 * likes_vector
                - 0.1 * dislikes_vector
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
                            {"key": "id", "match": {"value": post_id}}
                            for post_id in exclude_posts
                        ],
                        # Exclude posts authored by the user
                        {
                            "key": "authorable_id",
                            "match": {"value": user_id},  # Exclude user's own posts
                        },
                    ]
                },
            )

            posts = [
                {
                    "id": scored_point.id,
                    "score": scored_point.score,
                    "payload": scored_point.payload,
                }
                for scored_point in search_result
            ]

            return jsonify({"posts": posts})

        else:
            return jsonify({"error": f"Data not found for user {user_id}"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from qdrant_client.http import models

@app.route("/users/<int:user_id>/postsovertime", methods=["GET"])
def get_posts_over_time(user_id):
    try:
        # Use scroll with scroll_filter for filtering
        result, next_offset = client.scroll(
            collection_name="posts",
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="authorable_id",  # Field to filter on
                        match=models.MatchValue(value=user_id)  # Value to match
                    )
                ]
            ),
            limit=2000,  # Define the number of results per scroll
            with_payload=True,
            with_vectors=False
        )

        posts_over_time = [
            {
                "id": pt.id,
                "created_at": pt.payload.get("created_at") if pt.payload else None
            }
            for pt in result
        ]

        return jsonify(posts_over_time), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

        
@app.route("/users/<int:user_id>/recommendedusers", methods=["GET"])
def get_recommended_users(user_id):

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
            
            # Create a combined vector (you can adjust the weights as needed)
            combined_vector = (
                0.4 * posts_vector +
                0.3 * comments_vector +
                0.2 * likes_vector -
                0.1 * dislikes_vector
            )

            # Create NamedVector for the query, specifying which vector to compare against
            query_vector = NamedVector(name="posts_vector", vector=combined_vector.tolist())
            
            # Do semantic search against the collected_user_data collection
            search_result = client.search(
                collection_name="collected_user_data",
                query_vector=query_vector,
                query_filter={
                    "must_not": [
                        {
                            "key": "id",  
                            "match": {"value": user_id},  # Exclude the user's own profile
                        },
                    ],
                },
                limit=8  # Adjust the limit as needed
            )
            
            results = [
                {
                    'id': scored_point.id,
                    'score': scored_point.score,
                    #'payload': scored_point.payload
                } 
                for scored_point in search_result 
                if str(scored_point.id) != str(user_id)
            ][:20] 

            return (results, 200)
            
            # print(f"Id of the user {user_id}")
            # print(f"Results of the search {results}")
        else:
            print(f"No data found for user {user_id}")
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/trendingtopics", methods=["GET"])
def get_trending_topics():
    try:
        collected_post_result = client.scroll(
            collection_name="posts", with_payload=True, with_vectors=False
        )

        if not collected_post_result or len(collected_post_result) == 0:
            return jsonify({"error": "posts not found"}), 404

        collected_comment_result = client.scroll(
            collection_name="comments", with_payload=True, with_vectors=False
        )

        if not collected_post_result or len(collected_comment_result) == 0:
            return jsonify({"error": "comments not found"}), 404

        # Rest of OpenAI code...
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        Some collected data from a userbase will be provided. Return a list of 20
                        trending topics based on the data, following these rules:
                        
                        - They MUST be QUALITY topics, NOT just frequently mentioned words.
                        - Each topic MUST be EXACTLY one word.
                        - Capitalize the first letter of each topic.
                        - Topics MUST be RELEVANT to the userbase, NOT general or random.
                        - Output MUST be a JSON array with topics as strings WITHOUT a summary
                        - DO NOT provide any backticks or unnecessary whitespace, just provide RAW
                          JSON that can be dropped directly into code without any preprocessing

                        The data provided is as follows:
                        
                        {collected_post_result} {collected_comment_result}
                    """,
                }
            ],
        )

        topics = response.choices[0].message.content

        # No need to jsonify the response since it's already properly formatted
        return (topics, 200)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/user/<int:user_id>/interests/<string:topics>", methods=["GET"])
def get_user_interests(user_id, topics):
    try:
        collected_user_data = client.retrieve(
            collection_name="collected_user_data",
            ids=[user_id],
            with_payload=True,
            with_vectors=False,
        )

        # Rest of OpenAI code...
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        Some collected data from a user will be provided. 
                        Your first task is to return a list of 5 of their 
                        interests based on the data, following these rules:
                        
                        - They MUST be QUALITY interests, NOT just frequently mentioned words.
                        - Each interest must have a weight associated with its importance to 
                          the user, adding up to 100
                        - Each interest MUST be EXACTLY one word.
                        - Capitalize the first letter of each interests.
                        - Topics MUST be RELEVANT to the userbase, NOT general or random.
                        - Output MUST be a JSON array with interests as strings WITHOUT a summary
                        - DO NOT provide any backticks or unnecessary whitespace, just provide RAW
                          JSON that can be dropped directly into code without any preprocessing

                        Your second task will be to collect user opinion on a 
                        list of trending topics, following these rules:

                        - Weight each topic on a scale of -1 to 1, where -1 is highly likely to 
                          interact negatively, and 1 is highly likely to interact positively. 
                        - DO NOT provide any backticks or unnecessary whitespace, just provide RAW
                          JSON that can be dropped directly into code without any preprocessing

                        The data provided is as follows:
                        
                        {collected_user_data} {topics}
                    """,
                }
            ],
        )

        interests = response.choices[0].message.content

        # No need to jsonify the response since it's already properly formatted
        return (interests, 200)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users/count", methods=["GET"])
def get_user_count():
    try:
        collection_info = client.get_collection("collected_user_data")
        total_users = collection_info.points_count

        return jsonify({"total_users": total_users})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users", methods=["GET"])
def get_users():
    try:
        users_result = client.scroll(
            collection_name="users",
            limit=RECORDS_LIMIT,
            with_payload=True,
            with_vectors=False,
        )

        print(type(users_result[0]))

        # If no result is found, return 404
        if not users_result or len(users_result[0]) == 0:
            return jsonify({"error": "Users not found"}), 404

        users = {}

        for user in users_result[0]:
            users[user.payload['id']] = user.payload

        # Return the filtered user data as a JSON response
        return jsonify({'user_results': users}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API endpoint to get user data by user ID from the Qdrant collection
@app.route('/user/<int:user_id>/summary', methods=['GET'])
def get_user_summary(user_id):
    try:
        # Retrieve user data from Qdrant using the user ID
        collected_data_result = client.retrieve(
        collection_name="collected_user_data",
        ids=[user_id],
        with_payload=True,
        with_vectors=False
    )
        # Pass user data to OpenAI 
        openai_prompt = f"""This is collected data from a user. 
                            Make me a summary about this user in json format. 
                            Answer these questions as keys, in the form of paragraphs: 
                            What can you tell about the types of posts, comments, likes, and dislikes they make? keyname: summary
                            What is their overall attitude? keyname: overall_attitude
                            What are they likely to engage with? keyname: likely_engagement
                            {collected_data_result[0].payload}"""

        # Rest of OpenAI code...
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": openai_prompt,
            }],
        )

        return jsonify(response.choices[0].message.content), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        # Retrieve user data from Qdrant using the user ID
        user_data = client.retrieve(
            collection_name="users",
            ids=[user_id],
            with_payload=True,
            with_vectors=False,
        )

        print(user_data)

        # If no result is found, return 404
        if not user_data or len(user_data) == 0:
            return jsonify({"error": "User not found"}), 404

        # Return the user data as a JSON response
        return jsonify(user_data[0].payload), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
