from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from .env.local file
load_dotenv('..//.env.local')

Q_URL = os.getenv('Q_URL')
Q_KEY = os.getenv('Q_KEY')

# Initialize the client (adjust the URL and API key as needed)
client = QdrantClient(
    url=Q_URL, 
    api_key= Q_KEY,
)

user_id = 1 
vector_dimension = 384  # Adjust this if your vectors have a different dimension
default_vector = [0.0] * vector_dimension

def retrieve_like_ids(user_id: int, limit: int):
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
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    user_likes_ids = [point.payload.get('likeable_id', '')for point in likes_result[0]]

    return user_likes_ids

def retrieve_dislike_ids(user_id: int, limit: int):
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
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    user_dislikes_ids = [point.payload.get('dislikeable_id', '')for point in dislikes_result[0]]

    return user_dislikes_ids

likes = retrieve_like_ids(user_id, 3000)
dislikes = retrieve_dislike_ids(user_id, 100)

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
        

        print(f"Id of the user {user_id}")
        print(f"Results of the search {results}")
    else:
        print(f"No data found for user {user_id}")
        
except Exception as e:
    print(f"Error: {e}")