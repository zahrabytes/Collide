from .secrets import QDRANT_URL, QDRANT_API_KEY
from qdrant_client import QdrantClient

def initialize_qdrant_client() -> QdrantClient:
	client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
	return client