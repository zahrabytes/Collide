import json
import pandas as pd
import numpy as np
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

client = QdrantClient(
    url="https://33058675-b93f-4a25-add3-6391fac8678c.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="Ymack1QsKvvS7VqnC8jXd-g7reVcvQVpwrQmIuClLguPRR0xn_xohQ",
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
