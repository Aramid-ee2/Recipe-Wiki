# To be able to access the bucket
from google.cloud import storage
import hashlib


class Backend:

    # Class prefix variable
    SALT = "Heqodap12"

    def __init__(self, storage_client):
        self.storage_client = storage_client
        # Initialize access to all buckets
        self.users_bucket = self.storage_client.bucket('users_project1')
        self.wiki_info_bucket = self.storage_client.bucket('wiki_info_project1')
        self.authors_buckets = self.storage_client.bucket("recipe_authors")

    def get_wiki_page(self, name):
        #calling the list_blobs method on storage_client to list all the blobs stored in the wiki_info_project1 and store it in "blobs"
        blobs = self.storage_client.list_blobs("wiki_info_project1")
        for blob in blobs:
            #iterating through blobs to check for the blob we want to get its data
            if blob.name == name:
                with blob.open("r") as f:
                    #After finding the blob, we open and read it's content and store it in data
                    data = f.read()
                    return data
                    #return data to the method that calls get_wiki_pqge method

    def get_all_page_names(self):
        #calling the list_blobs method on storage_client to list all the blobs stored in the wiki_info_project1 and store it in "blobs"
        blobs = self.storage_client.list_blobs("wiki_info_project1")
        #Creating an empty list to help store all the page names for pages in wiki_info_project1 bucket
        page_names = []
        for blob in blobs:
            #iterate over blobs inorder to append the pages name to page_names list
            page_names.append(blob.name)
        return page_names
        #return page_names to the method that calls get_all_page_names

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

    def sign_in(self, user_name, password):
        #retrieve a reference to blob object named respective user_names stored in Google Cloud storage
        blob = self.users_bucket.blob(user_name)
        #Hashing the password
        password = self.SALT + user_name + password
        password = hashlib.sha256(password.encode()).hexdigest()
        with blob.open("r") as f:
            #opening the blob and reading the content which is the password
            data = f.read()
            #Checks if hashed password matches the content of the blob (password in bucket)
            if data != password:
                return False
                #if the data is the same as the content of blob return True else return False
            return True

    def get_image(self, name):
        #get_image receives the image as a parameter to the method
        #calling the list_blobs method on storage_client to list all the blobs stored in the recipe_authors bucket and store it in "blob"
        blob = self.storage_client.list_blobs("recipe_authors")
        for b in blob:
            #going through blob to check for the image(name)
            if b.name == name:
                with b.open("rb") as f:
                    #open the blob(image file in bucket) in binary format, read the data and return it
                    data = f.read()
                    return data
