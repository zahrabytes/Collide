import requests
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../.env.local')

# Qdrant API key from environment variables
Q_KEY = os.getenv('Q_KEY')
Q_URL = os.getenv('Q_URL')

client = QdrantClient(
    url=Q_URL, 
    api_key=Q_KEY,
)

random_user_url = 'https://randomuser.me/api/'

def update_user_payload(user_id):
    response = requests.get(random_user_url)
    data = response.json()

    profile_data = {
        "profile_picture": data['results'][0]['picture']['large'],
        "username": data['results'][0]['login']['username'],
        "name": data['results'][0]['name']['first'] + " " + data['results'][0]['name']['last']
    }

    client.set_payload(
        collection_name="users",
        payload=profile_data,
        points=[user_id]
    )
    print(f"Updated payload for user {user_id}")

# Scroll through the collection to retrieve all users
offset = None
limit = 5000  # Adjust this value based on your needs and server capabilities

while True:
    collected_data_result = client.scroll(
        collection_name="users",
        with_payload=True,
        with_vectors=False,
        limit=limit,
        offset=offset
    )

    users, next_offset = collected_data_result

    for user in users:
        update_user_payload(user.id)

    if next_offset is None:
        break

    offset = next_offset

print("Finished updating all users")