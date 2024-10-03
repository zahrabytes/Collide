from shared import initialize_qdrant_client, make_openai_request

class TrendingTopicsService:
	def __init__(self):
		self.q_client = initialize_qdrant_client()

	def get_trending_topics(self) -> str:

		posts = self._get_all_posts()
		comments = self._get_all_comments()

		openai_prompt = f"""
				Some collected data from a userbase will be provided. Return a list of 20
				trending topics based on the data, following these rules:

				- They MUST be QUALITY topics, NOT just frequently mentioned words.
				- Each topic MUST be EXACTLY one word.
				- Capitalize the first letter of each topic.
				- Topics MUST be RELEVANT to the userbase, NOT general or random.
				- Output MUST be a JSON array with topics as strings WITHOUT a summary
				- DO NOT provide any backticks or unnecessary whitespace, just provide RAW
				  JSON that can be dropped directly into code without any preprocessing

				The data provided is as follows:

				{posts} {comments}
			"""

		trending_topics = make_openai_request(openai_prompt)

		return trending_topics

	# Private method
	def _get_all_posts(self) -> tuple:

		try:
			posts_result = self.q_client.scroll(
			    collection_name='posts', with_payload=True, with_vectors=False
			)
		except Exception as e:
			return self._exception_handler(e)

		if posts_result:
			return posts_result

		return

	# Private method
	def _get_all_comments(self) -> tuple:

		try:
			comments_result = self.q_client.scroll(
		        collection_name='comments', with_payload=True, with_vectors=False
		    )
		except Exception as e:
			return _exception_handler(e)

		if comments_result:
			return comments_result

		return

	# Private method
	def _exception_handler(self, exception: Exception) -> None:
		# A logger could be integrated instead of print statements
		print(f'Error with trending topics service {exception}')
		return



