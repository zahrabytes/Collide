import json
import pandas as pd
import numpy as np
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

client = QdrantClient(
    url=SECRET_URL, 
    api_key=SECRET_KEY,
)

model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to remove null values (as defined earlier)
def remove_null_values(obj):
    if isinstance(obj, dict):
        return {k: remove_null_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_null_values(v) for v in obj if v is not None]
    else:
        return obj

with open('dislikes.json', 'r') as f:
    data = json.load(f)

# Extract likes data
dislikes = data['dislikes']

# Prepare data for upsert
points = [
    {
        "id": dislike['id'],
        "vector": [0.0] * 384,  # Dummy vector; replace with actual vectors if available
        "payload": {
            "authorable_type": dislike["authorable_type"],
            "authorable_id": dislike["authorable_id"],
            "dislikeable_type": dislike["dislikeable_type"],
            "dislikeable_id": dislike["dislikeable_id"],
            "created_at": dislike["created_at"],
            "updated_at": dislike["updated_at"]
        }
    }
    for dislike in dislikes
]

# Upsert the likes data
client.upsert(
    collection_name="dislikes",
    points=points
)

print("Dislikes data inserted successfully!")


with open('likes.json', 'r') as c:
    data = json.load(c)

# Extract likes data
likes = data['likes']

# Prepare data for upsert
points = [
    {
        "id": like['id'],
        "vector": [0.0] * 384,  # Dummy vector; replace with actual vectors if available
        "payload": {
            "authorable_type": like["authorable_type"],
            "authorable_id": like["authorable_id"],
            "likeable_type": like["likeable_type"],
            "likeable_id": like["likeable_id"],
            "created_at": like["created_at"],
            "updated_at": like["updated_at"]
        }
    }
    for like in likes
]

# Upsert the likes data
client.upsert(
    collection_name="likes",
    points=points
)

print("Likes data inserted successfully!")

######## Concatenating user Data ######## 

def find_users(limit: int):

    user_ids = []

    users_result = client.scroll(
        collection_name="users",
        limit=5000,
        with_payload=False,
        with_vectors=False
    )

    user_ids = [point.id for point in users_result[0]]

    return user_ids

def search_user_posts(user_id: int, limit: int):

    posts_result = client.scroll(
        collection_name="posts",
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

    posts_list = [
    {
        'title': point.payload.get('title', ''),
        'body': point.payload.get('plain_text_body', '')
    }
    for point in posts_result[0] 
    if point.payload
    ]

    posts = ' '.join([f"{post['title']} {post['body']}".strip() for post in posts_list])

    return posts

def search_user_comments(user_id: int, limit: int):

    comments_result = client.scroll(
        collection_name="comments",
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

    comments_list = [point.payload.get('body', '') for point in comments_result[0] if point.payload]
    comments = ' '.join(comments_list)

    return comments


def search_user_likes(user_id: int, limit: int):
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

    liked_content = []
    for point in likes_result[0]:
        if 'likeable_type' in point.payload and 'likeable_id' in point.payload:
            if point.payload['likeable_type'] == 'Post':
                post = client.retrieve(
                    collection_name="posts",
                    ids=[point.payload['likeable_id']],
                    with_payload=True,
                    with_vectors=False
                )
                if post:
                    title = post[0].payload.get('title', '')
                    body = post[0].payload.get('plain_text_body', '')
                    liked_content.append(f"{title} {body}".strip())
            elif point.payload['likeable_type'] == 'Comment':
                comment = client.retrieve(
                    collection_name="comments",
                    ids=[point.payload['likeable_id']],
                    with_payload=True,
                    with_vectors=False
                )
                if comment:
                    body = comment[0].payload.get('body', '')
                    liked_content.append(body)

    return ' '.join(liked_content)


def search_user_dislikes(user_id: int, limit: int):
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

    disliked_content = []
    for point in dislikes_result[0]:
        if 'dislikeable_type' in point.payload and 'dislikeable_id' in point.payload:
            if point.payload['dislikeable_type'] == 'Post':
                post = client.retrieve(
                    collection_name="posts",
                    ids=[point.payload['dislikeable_id']],
                    with_payload=True,
                    with_vectors=False
                )
                if post:
                    title = post[0].payload.get('title', '')
                    body = post[0].payload.get('plain_text_body', '')
                    disliked_content.append(f"{title} {body}".strip())
            elif point.payload['dislikeable_type'] == 'Comment':
                comment = client.retrieve(
                    collection_name="comments",
                    ids=[point.payload['dislikeable_id']],
                    with_payload=True,
                    with_vectors=False
                )
                if comment:
                    body = comment[0].payload.get('body', '')
                    disliked_content.append(body)

    return ' '.join(disliked_content)


def insert_collected_data(user_id: int, posts: str, likes: str, dislikes: str, comments: str):
    try:
        # Prepare data for vectorization
        data_to_vectorize = {
            "posts_vector": posts,
            "comments_vector": comments,
            "likes_vector": likes,
            "dislikes_vector": dislikes
        }
        
        # Vectorize non-empty strings
        vectors = {
            key: model.encode(value).tolist() 
            for key, value in data_to_vectorize.items() 
            if value.strip()
        }
        
        point = [{
            "id": user_id,
            "vector": vectors,
            "payload": {
                "posts": posts,
                "comments": comments,
                "likes": likes,
                "dislikes": dislikes,
            }
        }]

        # Upsert collected user data
        result = client.upsert(
            collection_name="collected_user_data",
            points=point
        )
        print(f"Data inserted for user {user_id}: {result}")
    except Exception as e:
        print(f"Error inserting data for user {user_id}: {e}")


limit = 5000

user_ids = find_users(limit)

for user_id in user_ids:

    posts = search_user_posts(user_id, limit)

    likes = search_user_likes(user_id, limit)

    dislikes = search_user_dislikes(user_id, limit)

    comments = search_user_comments(user_id, limit)

    insert_collected_data(user_id, posts, likes, dislikes, comments)
