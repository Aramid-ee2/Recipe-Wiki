# TODO(Project 1): Implement Backend according to the requirements.
# To be able to access the bucket
from google.cloud import storage
import hashlib
class Backend:

    def __init__(self):
        self.storage_client = storage.Client()
        # Initialize access to both buckets
        self.users_bucket = self.storage_client.bucket('users_project1')
        self.wiki_info_bucket = self.storage_client.bucket('wiki_info_project1')  
        self.authors_buckets = self.storage_client.bucket("recipe_authors")      
       
        
    def get_wiki_page(self, name):
        blobs = self.storage_client.list_blobs("wiki_info_project1")
        for blob in blobs:
            if blob.name == name:
                with blob.open("r") as f:
                    data = f.read()
                    return data
       

    def get_all_page_names(self):
        #self.storage_client.list_blobs("wiki_info_project1")
    
        blobs = self.storage_client.list_blobs("wiki_info_project1")
        page_names = []
        for blob in blobs:
            page_names.append(blob.name)
        return page_names

        

    def upload(self, file):
        # File.filename returns name of the file
        blob = self.wiki_info_bucket.blob(file.filename)
        # Upload actual file to bucket
        blob.upload_from_file(file, content_type=file.content_type)

    def sign_up(self, user_name, password):
        # Reach out to GCS and create user_name file that contains the password
        blob = self.users_bucket.blob(user_name)
        #TODO: Add username to password hash so different users with same password get different hash value
        with blob.open("w") as f:
            # Add prefix and hash password
            password = "protection" + password
            f.write(hashlib.sha256(password).hexdigest())
        

    def sign_in(self, user_name, password):
        #Checks if hashed password matches password in bucket 
        blob = self.users_bucket.blob(user_name)
        #TODO: Check if hashing is done properly
        password = f"{user_name} protection {password}"
        password = hashlib.sha256(password.encode()).hexdigest()
        with blob.open("r") as f:
            data = f.read()
            if data != password:
                return False
            return True

        
    def get_image(self, name):
        #TODO: Get image of teammates and display in about page, get_image gets the image data from bucket and send it to frontend
        blob = self.storage_client.list_blobs("recipe_authors")
        for b in blob:
            if b.name == name:
                with b.open("rb") as f:
                    data = f.read()
                    #image = data.download_as_bytes()
                    return data