# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
class Backend:

    def __init__(self):
        storage_client = storage.Client()
        self.users_bucket = storage_client.bucket('users_project1')
        self.wiki_info_bucket = storage_client.bucket('wiki_info_project1')
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self, user_name, password):
        # Reach out to GCS and create user with username and password
        blob = self.users_bucket.blob(user_name)
        with blob.open("w") as f:
            # TODO: add prefix and hash password
            f.write(password)
        
    def sign_in(self):
        pass

    def get_image(self):
        pass

