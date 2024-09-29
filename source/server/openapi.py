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

user_id = 1

def get_user_summary(user_id: int) -> dict:

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

    return(response.choices[0].message.content)
    
get_user_summary(user_id)