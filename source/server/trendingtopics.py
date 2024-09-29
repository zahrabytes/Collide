from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env.local file
load_dotenv('..//.env.local')

Q_URL = os.getenv('Q_URL')
Q_KEY = os.getenv('Q_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')

openai.api_key=OPENAI_KEY

# Initialize the client (adjust the URL and API key as needed)
client = QdrantClient(
    url=Q_URL, 
    api_key= Q_KEY,
)

user_id = 3495

def get_user_collected_data(user_id: int) -> dict:

    collected_post_result = client.scroll(
        collection_name="posts",
        with_payload=True,
        with_vectors=False
    )
    
    collected_post_result = client.scroll(
        collection_name="comments",
        with_payload=True,
        with_vectors=False
    )

    # Rest of OpenAI code...
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"This is collected data from a userbase. Give me a list of 20 trending topics (they must be quality topics, not just frequently mentioned words, two words each, in list separated by commas, without summarry): {collected_post_result} {collected_post_result}",
        }],
    )

    print(response.choices[0].message.content)
get_user_collected_data(user_id)