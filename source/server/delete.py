import json
import pandas as pd
import numpy as np
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('../.env.local')

# Qdrant API key from environment variables
Q_KEY = os.getenv('Q_KEY')
Q_URL = os.getenv('Q_URL')

client = QdrantClient(
    url=Q_URL, 
    api_key=Q_KEY,
)

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_users():

    user_ids = []

    users_result = client.scroll(
        collection_name="collected_user_data",
        limit=5000,
        with_payload=True,
        with_vectors=False
    )

    excluded_payload = {
        "posts": "",
        "comments": "",
        "likes": "",
        "dislikes": ""
    }

    for user in users_result[0]:
        if user.payload == excluded_payload:
            user_ids.append(user.id)

   
    # Delete users from the collection
    client.delete(
        collection_name="collected_user_data",
        points_selector=models.PointIdsList(
            points=user_ids,
        ),
    )
        

    return user_ids


print(find_users())