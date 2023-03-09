# TODO(Project 1): Implement Backend according to the requirements.
# To be able to access the bucket
from google.cloud import storage
import hashlib
class Backend:

    # Class prefix variable
    SALT = "Heqodap12"

    def __init__(self, storage_client):
        # Initialize access to both buckets
        self.users_bucket = storage_client.bucket('users_project1')
        self.wiki_info_bucket = storage_client.bucket('wiki_info_project1')
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self, file):
        # File.filename returns name of the file
        blob = self.wiki_info_bucket.blob(file.filename)
        # Upload actual file to bucket
        blob.upload_from_file(file, content_type=file.content_type)

    def sign_up(self, user_name, password):
        # Reach out to GCS and create user_name file that contains the password
        blob = self.users_bucket.blob(user_name)
        # Add prefix and hash password
        with blob.open("w") as f:
            #Add username to password hash so different users with same password get different hash value
            encoded = self.SALT + user_name + password
            f.write(hashlib.sha256(encoded.encode()).hexdigest())  

    def sign_in(self, username, password):
        #Checks if hashed password matches password in bucket 
        blob = self.users_bucket.blob(username)
        password = self.SALT + password
        password = hashlib.blake2b(password.encode()).hexdigest()
        with blob.open("r") as f:
            data = f.read()
            if data != password:
                return False
            return True

        
    def get_image(self):
        pass

