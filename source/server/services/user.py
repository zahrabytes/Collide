import numpy as np
from numpy import ndarray
from qdrant_client.models import NamedVector
from qdrant_client.http.models import Record
from shared import initialize_qdrant_client, make_openai_request

class UserService:
	def __init__(self):
		self.q_client = initialize_qdrant_client()
		self.records_limit = 5000 # Limit to check through the entire collection
		self.recommended_posts_limit = 20 # Limit on recommended posts for each user
		self.recommended_users_limit = 20 # Limit on recommended users for each user
		self.default_vector = [0.0] * 384
		self.vector_weights = [0.4, 0.3, 0.2, 0.1]


	def get_user(self, user_id: int) -> list:
		try:
			user_data_result = self.q_client.retrieve(
	        collection_name='users',
	        ids=[user_id],
	        with_payload=True,
	        with_vectors=False,
	    )
		except Exception as e:
			return self._exception_handler(e)

		if user_data_result:
			user = user_data_result[0].payload
			return user

		return # If user not found return nothing


	def get_user_summary(self, user_id: int) -> dict:

		collected_user_data = self._retrieve_user_collected_data(user_id)

		if not collected_user_data:
			return

		openai_prompt = f"""
		        Data collected from a user will be provided. Make a summary about the user in JSON format. 

		        Answer these questions as keys, in the form of paragraphs: 
		        - What can you tell about the types of posts, comments, likes, and dislikes they make? keyname: summary
		        - What is their overall attitude? keyname: overall_attitude
		        - What are they likely to engage with? keyname: likely_engagement

		        Rules:
		        - DO NOT provide any backticks or unnecessary whitespace, just provide RAW
		          JSON that can be dropped directly into code without any preprocessing

		        The data provided is as follows: {collected_user_data}
			"""

		summary = make_openai_request(openai_prompt)

		return summary


	def get_recommended_users(self, user_id: int) -> list[dict]:

		collected_user_data = self._retrieve_user_collected_data(user_id)

		if not collected_user_data:
			return

		combined_embedding = self._get_combined_embedding(collected_user_data)

		# Create NamedVector for the query, specifying which vector to compare against
		query_vector = NamedVector(
		    name='posts_vector', vector=combined_embedding.tolist()
		)
		try: 
		    # Do semantic search against the collected_user_data collection
		    collected_user_data_search_result = self.q_client.search(
		        collection_name='collected_user_data',
		        query_vector=query_vector,
		        query_filter={
				        'must_not': [
				            {
				                'key': 'id',
				                'match': {
				                    'value': user_id
				                }
				            }
				        ]
				    },
		        limit=self.recommended_users_limit,
		    )
		except Exception as e:
			return self._exception_handler(e)

		recommmended_users_results = [
		        {
		            'id': scored_point.id,
		            'score': scored_point.score,
		        }
		        for scored_point in collected_user_data_search_result
		        if str(scored_point.id) != str(user_id)
		    ][:self.recommended_users_limit]

		print(recommmended_users_results)

		return recommmended_users_results


	def get_user_topics_match(self, user_id: int, topics: str) -> str:

		collected_user_data = self._retrieve_user_collected_data(user_id)

		if not collected_user_data:
			return

		openai_prompt = f"""
		        Some collected data from a user will be provided. Collect user opinion on a
		        list of trending topics (that will be provided), following these rules:

		        - Weigh each topic on a scale of -1 to 1, where -1 is highly likely to
		          interact negatively, and 1 is highly likely to interact positively.
		        - DO NOT provide any backticks or unnecessary whitespace, just provide RAW
		          JSON that can be dropped directly into code without any preprocessing
		        - ONLY INCLUDE the topics provided, DO NOT include any extra topics

		        Reponse must be in this format:
		        {{
		            "topic1": 0.5,
		            "topic2": -0.3,
		            "topic3": 0.9,
		            ...
		        }}

		        The data provided is as follows:

		        Collected user data: {collected_user_data}

		        Topics list: {topics}
		    """
		
		topics_match = make_openai_request(openai_prompt)

		return topics_match


	def get_user_interests(self, user_id: int) -> str:

		collected_user_data = self._retrieve_user_collected_data(user_id)

		if not collected_user_data:
			return

		openai_prompt = f"""
                Some collected data from a user will be provided. Your task is to return a list
                of 5 of their  interests based on the data, following these rules:
                
                - They MUST be QUALITY interests, NOT just frequently mentioned words.
                - Each interest must have a weight associated with its importance to 
                  the user, adding up to 100
                - Each interest MUST be EXACTLY one word.
                - Capitalize the first letter of each interests.
                - Topics MUST be RELEVANT to the userbase, NOT general or random.
                - Output MUST be a JSON array with interests as strings WITHOUT a summary
                - DO NOT provide any backticks or unnecessary whitespace, just provide RAW
                  JSON that can be dropped directly into code without any preprocessing

                Reponse must be in this format:

                {{
                    "interest1": 20,
                    "interest2": 30,
                    "interest3": 10,
                    ...
                }}

                The data provided is as follows: {collected_user_data}
            """
		
		interests = make_openai_request(openai_prompt)

		return interests


	def get_recommended_posts(self, user_id: int) -> list[dict]:

		collected_user_data = self._retrieve_user_collected_data(user_id)

		if not collected_user_data:
			return

		combined_embedding = self._get_combined_embedding(collected_user_data)

		user_liked_content_ids = self._retrieve_user_liked_content_ids(user_id)
		user_disliked_content_ids = self._retrieve_user_disliked_content_ids(user_id)
		posts_to_exclude = user_liked_content_ids + user_disliked_content_ids

		try:
			# Get recommended posts by semantic searching against posts collection
		    recommended_posts_result = self.q_client.search(
		        collection_name="posts",
		        query_vector=combined_embedding,
		        limit=self.recommended_posts_limit,
		        query_filter={
		            "must_not": [
		                # Exclude posts with ids from likes and dislikes
		                *[
		                    {"key": "id", "match": {"value": post_id}}
		                    for post_id in posts_to_exclude
		                ],
		                # Exclude user's own posts
		                {
		                    "key": "authorable_id",
		                    "match": {"value": user_id},  
		                },
		            ]
		        },
		    )
		except Exception as e:
			return self._exception_handler(e)

		recommended_posts = [
		    {
		        'id': scored_point.id,
		        'score': scored_point.score,
		        'payload': scored_point.payload,
		    }
		    for scored_point in recommended_posts_result
		]

		return recommended_posts


	# Private method
	def _get_combined_embedding(self, collected_user_data: Record) -> ndarray:
		# Safely get vectors, using the default if a vector is missing or empty
		posts_vector = np.array(
		    collected_user_data.vector.get('posts_vector', self.default_vector) or self.default_vector
		)
		comments_vector = np.array(
		    collected_user_data.vector.get('comments_vector', self.default_vector) or self.default_vector
		)
		likes_vector = np.array(
		    collected_user_data.vector.get('likes_vector', self.default_vector) or self.default_vector
		)
		dislikes_vector = np.array(
		    collected_user_data.vector.get('dislikes_vector', self.default_vector) or self.default_vector
		)

		# Combine embeddings
		combined_embedding = (
		    0.4 * posts_vector
		    + 0.3 * comments_vector
		    + 0.2 * likes_vector
		    - 0.1 * dislikes_vector
		)

		# No need to do error handling. Already taken care of inside the collected_user_data function
		return combined_embedding


	# Private method
	def _retrieve_user_collected_data(self, user_id: int) -> Record:

		try: 
			collected_user_data_result = self.q_client.retrieve(
				collection_name="collected_user_data",
				ids=[user_id],
				with_payload=True,
				with_vectors=True
			)
		except Exception as e:
			self._exception_handler(e)

		if collected_user_data_result:
			collected_user_data = collected_user_data_result[0]
			return collected_user_data

		return


	# Private method
	def _retrieve_user_liked_content_ids(self, user_id: int) -> list:

		try:
		    likes_result = self.q_client.scroll(
		        collection_name="likes",
		        scroll_filter={
		        	"must": [
		        		{
		        			"key": "authorable_id", 
		        			"match": {"value": user_id}
		        		}
		        	]
		        },
		        limit=self.records_limit,
		        with_payload=True,
		        with_vectors=False
		    )
		except Exception as e:
			return self._exception_handler(e)

		if likes_result:
			user_liked_content_ids = [point.payload.get("likeable_id", "") for point in likes_result[0]]
			return user_liked_content_ids

		return


	# Private method
	def _retrieve_user_disliked_content_ids(self, user_id: int) -> list:

		try:
		    dislikes_result = self.q_client.scroll(
		        collection_name="dislikes",
		        scroll_filter={
			        "must": [
			        	{
			        		"key": "authorable_id", 
			        		"match": {"value": user_id}
			        	}
				    ]
				},
		        limit=self.records_limit,
		        with_payload=True,
		        with_vectors=False
		    )
		except Exception as e:
			return self._exception_handler(e)

		if dislikes_result:
			user_disliked_content_ids = [point.payload.get("dislikeable_id", "") for point in dislikes_result[0]]
			return user_disliked_content_ids

		return


	# Private method
	def _exception_handler(self, exception: Exception) -> None:
		# A logger could be integrated instead of print statements
		print(f'Error with user service {exception}')
		return

		