from openai import OpenAI
from .secrets import OPENAI_KEY

OPENAI_MODEL = 'gpt-4o-mini'

def initialize_openai_client() -> OpenAI:
	client = OpenAI(api_key=OPENAI_KEY)
	return client

def make_openai_request(prompt: str) -> str:

	client = initialize_openai_client()

	openai_response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{'role': 'user', 'content': prompt}]
    )

	openai_response_content = openai_response.choices[0].message.content

	return openai_response_content