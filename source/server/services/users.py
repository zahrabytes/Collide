from shared import initialize_qdrant_client

class UsersService:
    def __init__(self):
        self.q_client = initialize_qdrant_client()
        self.records_limit = 5000


    def get_all_users(self) -> tuple:

        try:
            users_result = self.q_client.scroll(
                collection_name='users',
                limit=self.records_limit,
                with_payload=True,
                with_vectors=False,
            )
        except Exception as e:
            return self._exception_handler(e)

        if users_result:
            return users_result

        return


    # Private method
    def _exception_handler(self, exception: Exception) -> None:
        # A logger could be integrated instead of print statements
        print(f'Error with user service {exception}')
        return
