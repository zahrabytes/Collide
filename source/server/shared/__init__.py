from .database import initialize_qdrant_client
from .ai import make_openai_request

# Only export internal modules when doing 'from shared import *'
__all__ = ['initialize_qdrant_client', 'make_openai_request']