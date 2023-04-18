# To be able to access the bucket
from google.cloud import storage
import hashlib
import json
from flask_login import current_user


class Backend:

    # Class prefix variable
    SALT = "Heqodap12"

    def __init__(self, storage_client):
        self.storage_client = storage_client
        # Initialize access to all buckets
        self.users_bucket = self.storage_client.bucket('users_project1')
        self.wiki_info_bucket = self.storage_client.bucket('wiki_info_project1')
        self.authors_buckets = self.storage_client.bucket("recipe_authors")
        self.reviews_bucket = self.storage_client.bucket("page_reviews")

    # TODO: update method to search file from selected language (default english)
    def get_wiki_page(self, name):
        # calling the list_blobs method on storage_client to list all the blobs stored in the wiki_info_project1 and store it in "blobs"
        blobs = self.storage_client.list_blobs("wiki_info_project1")
        for blob in blobs:
            # iterating through blobs to check for the blob we want to get its data
            if blob.name == name:
                with blob.open("r") as f:
                    # After finding the blob, we open and read it's content and store it in data
                    data = f.read()
                    return data
                    # return data to the method that calls get_wiki_pqge method

    # TODO: Update this method to include users preferred language
    def get_all_page_names(self):
        # calling the list_blobs method on storage_client to list all the blobs stored in the wiki_info_project1 and store it in "blobs"
        blobs = self.storage_client.list_blobs("wiki_info_project1")
        # Creating an empty list to help store all the page names for pages in wiki_info_project1 bucket
        page_names = []
        for blob in blobs:
            # iterate over blobs inorder to append the pages name to page_names list
            page_names.append(blob.name)
        return page_names
        # return page_names to the method that calls get_all_page_names

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
            # Add username to password hash so different users with same password get different hash value
            encoded = self.SALT + user_name + password
            password = hashlib.sha256(encoded.encode()).hexdigest()
            user_settings = {
                "Password": password,
                "Language": "English",
                "Night_Mode": False,
                "Bookmarks": []
            }
            json_object = json.dumps(user_settings)
            f.write(json_object)

    def sign_in(self, user_name, password):
        # retrieve a reference to blob object named respective user_names stored in Google Cloud storage
        blob = self.users_bucket.blob(user_name)
        # Hashing the password
        password = self.SALT + user_name + password
        password = hashlib.sha256(password.encode()).hexdigest()
        with blob.open("r") as f:
            # Retrieving password from json file in GCS
            json_object = f.read()
            user_info = json.loads(json_object)
            user_password = user_info["Password"]
            # Checks if hashed password matches the content of the blob (password in bucket)
            if user_password != password:
                return False
                # if the data is the same as the content of blob return True else return False
            return True

    def get_image(self, name):
        # get_image receives the image as a parameter to the method
        # calling the list_blobs method on storage_client to list all the blobs stored in the recipe_authors bucket and store it in "blob"
        blob = self.storage_client.list_blobs("recipe_authors")
        for b in blob:
            # going through blob to check for the image(name)
            if b.name == name:
                with b.open("rb") as f:
                    # open the blob(image file in bucket) in binary format, read the data and return it
                    data = f.read()
                    return data

    def update_language(self, new_language, current_user=current_user):
        # Retrieve user blob.
        blob = self.users_bucket.blob(current_user.get_id())
        json_object = blob.download_as_string()
        user_info = json.loads(json_object)
        user_info["Language"] = new_language
        # Update GCS
        with blob.open("w") as f:
            json_object = json.dumps(user_info)
            f.write(json_object)

    def update_night_mode(self, current_user=current_user):
        # Retrieve user blob.
        blob = self.users_bucket.blob(current_user.get_id())
        # Reading blob
        json_object = blob.download_as_string()
        user_info = json.loads(json_object)
        if user_info["Night_Mode"]:
            user_info["Night_Mode"] = False
        else:
            user_info["Night_Mode"] = True
        # Update GCS
        with blob.open("w") as f:
            json_object = json.dumps(user_info)
            f.write(json_object)

    # def update_bookmarks(self, new_page):
    #     # Retrieve user blob.
    #     blob = self.users_bucket.blob(current_user.get_id())
    #     # Reading blob
    #     json_object = blob.download_as_string()
    #     user_info = json.loads(json_object)
    #     # Pass list through a set to prevent duplicate pages from being added
    #     temp = set(user_info["Bookmarks"])
    #     temp.add(new_page)
    #     # Turn back into list for json file
    #     new_list = list(temp)
    #     user_info["Bookmarks"] = new_list
    #     # Update GCS
    #     with blob.open("w") as f:
    #         json_object = json.dumps(user_info)
    #         f.write(json_object)

    def get_current_settings(self, current_user=current_user):
        if not current_user.get_id():
            user_info = {
                "Language": "English",
                "Night_Mode": False,
                "Bookmarks": []
            }
            return user_info
        else:
            # Retrieve user blob.
            blob = self.users_bucket.blob(current_user.get_id())
            # Reading blob
            json_object = blob.download_as_string()
            user_info = json.loads(json_object)
            user_info.pop("Password")
            # If user has not been created yet
            return user_info

    def update_review(self, review, wiki_page):
        blob = self.reviews_bucket.blob(wiki_page)
        # Check if exists
        if blob.exists():
            json_object = blob.download_as_string()
            reviews_list = json.loads(json_object)
            reviews_list.append(review)
            # Update GCS
            with blob.open("w") as f:
                json_object = json.dumps(reviews_list)
                f.write(json_object)
        else:
            # If no reviews exist yet
            reviews_list = [review]
            with blob.open("w") as f:
                json_object = json.dumps(reviews_list)
                f.write(json_object)

    def view_current_reviews(self, wiki_page):
        blob = self.reviews_bucket.blob(wiki_page)
        # Check if exists
        if blob.exists():
            json_object = blob.download_as_string()
            reviews_list = json.loads(json_object)
            sum_list = sum(reviews_list)
            average = round(sum_list / len(reviews_list), 1)
            return average
        else:
            # If no reviews exist yet
            return 0
