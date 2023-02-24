# TODO(Project 1): Implement Backend according to the requirements.
# To be able to access the bucket
from google.cloud import storage
class Backend:

    def __init__(self):
        storage_client = storage.Client()
        # Initialize access to both buckets
        self.users_bucket = storage_client.bucket('users_project1')
        self.wiki_info_bucket = storage_client.bucket('wiki_info_project1')
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self, user_name, password):
        # Reach out to GCS and create user_name file that contains the password
        blob = self.users_bucket.blob(user_name)
        with blob.open("w") as f:
            # TODO: add prefix and hash password
            password = "protection" + password
            f.write(password.hash())
        
    def sign_in(self):
        pass

    def get_image(self):
        pass

