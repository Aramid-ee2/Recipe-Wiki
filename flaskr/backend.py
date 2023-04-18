# To be able to access the bucket
from google.cloud import storage
import hashlib, json, string, re
from flask_login import current_user
from bs4 import BeautifulSoup


class Backend:

    # Class prefix variable
    SALT = "Heqodap12"

    def __init__(self, storage_client, opener=open):
        self.open = opener
        self.storage_client = storage_client
        # Initialize access to all buckets
        self.users_bucket = self.storage_client.bucket('users_project1')
        self.wiki_info_bucket = self.storage_client.bucket('wiki_info_project1')
        self.authors_buckets = self.storage_client.bucket("recipe_authors")
        self.wiki_search_content = self.storage_client.bucket(
            "wiki_search_content")

    # TODO: update method to search file from selected language (default english)
    def get_wiki_page(self, name, user_details):
        #blobs = self.storage_client.list_blobs("wiki_info_project1")
        if user_details.get_id():
            blob = self.users_bucket.blob(user_details.get_id())
            json_object = blob.download_as_string()
            user_info = json.loads(json_object)
            preffered_language = user_info.get("Language")
        else:
            preffered_language = 'English'

        blobs = self.wiki_info_bucket.list_blobs(prefix=preffered_language +
                                                 '/')
        for blob in blobs:
            if blob.name == preffered_language + '/' + name:
                with blob.open("r") as f:
                    data = f.read()
                    return data

    #TODO: Update this method to include users preferred language
    def get_all_page_names(self, user_details):
        page_names = []
        #print(current_user)
        #To load recipe pages based on user's preffered language user blob needs to be retrieved.
        if user_details.get_id():
            blob = self.users_bucket.blob(user_details.get_id())
            # Reading blob
            json_object = blob.download_as_string()
            user_info = json.loads(json_object)
            preffered_language = user_info.get("Language")
        else:
            preffered_language = 'English'
        #calling the list_blobs method on storage_client to list all the blobs stored in the wiki_info_project1 and store it in "blobs"
        blobs = self.wiki_info_bucket.list_blobs(prefix=preffered_language +
                                                 '/')
        for blob in blobs:
            #iterate over blobs inorder to append the pages name to page_names list
            name = blob.name.split('/')
            page_names.append(name[-1])
        return page_names

    def file_content_blob(self, blob):
        with blob.open("r") as new:
            recipe_content = new.read()
            return recipe_content

    def file_content_file(self, file):
        with self.open(file, 'r') as new:
            recipe_content = new.read()
            return recipe_content

    def create_inverted_index(self, file, inverted_index, file_name,
                              recipe_content):
        stop_words = {
            'the', 'or', 'in', 'is', 'a', 'an', 'of', 'at', 'from', 'to'
        }
        soup = BeautifulSoup(recipe_content, "html.parser")
        text_content = soup.get_text()
        filtered = re.findall(r'\w+', text_content)
        for word in filtered:
            if word.lower() not in stop_words:
                if word.lower() not in inverted_index:
                    inverted_index[word.lower()] = [file_name]
                else:
                    if file_name not in inverted_index[word.lower()]:
                        inverted_index[word.lower()].append(file_name)
        return inverted_index

    def upload(self, file):
        # File.filename returns name of the file
        blob = self.wiki_info_bucket.blob(file.filename)
        # Upload actual file to bucket
        blob.upload_from_file(file, content_type=file.content_type)
        blob = self.wiki_search_content.blob("inverted_index")
        if not blob:
            self.initial_index()
        with blob.open("r") as f:
            # Retrieving inverted index from json file in GCS
            json_index = f.read()
            inverted_index = json.loads(json_index)
            recipe_content = self.file_content_file(file)
            updated = self.create_inverted_index(file, inverted_index,
                                                 file.filename, recipe_content)
            #Writing the updated inverted index to gcs as a json string
            json_index = json.dumps(updated)
            # Reach out to GCS to access bucket where inverted index is stored and rewrite to it
            f.write(json_index)

    def sign_up(self, user_name, password):
        # Reach out to GCS and create user_name file that contains the password
        blob = self.users_bucket.blob(user_name)
        # Add prefix and hash password
        with blob.open("w") as f:
            #Add username to password hash so different users with same password get different hash value
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
        #retrieve a reference to blob object named respective user_names stored in Google Cloud storage
        blob = self.users_bucket.blob(user_name)
        #Hashing the password
        password = self.SALT + user_name + password
        password = hashlib.sha256(password.encode()).hexdigest()
        with blob.open("r") as f:
            # Retrieving password from json file in GCS
            json_object = f.read()
            user_info = json.loads(json_object)
            user_password = user_info["Password"]
            #Checks if hashed password matches the content of the blob (password in bucket)
            if user_password != password:
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

    #TODO: Figure how to extract texts from html files
    def initial_index(self):
        inverted_index = {}
        #Call list_blobs method to get all the blobs in wiki info bucket so I can index their respective contents
        blobs = self.wiki_info_bucket.list_blobs(prefix="English/")
        for blob in blobs:
            recipe_content = self.file_content_blob(blob)
            inverted_index = self.create_inverted_index(blob, inverted_index,
                                                        blob.name,
                                                        recipe_content)

        #Writing the inverted index to gcs as a json string
        json_index = json.dumps(inverted_index)
        # Reach out to GCS to access bucket where inverted index would be stored
        blob = self.wiki_search_content.blob("inverted_index")
        with blob.open("w") as index:
            index.write(json_index)

    # TODO test
    def update_language(self, new_language):
        # Retrieve user blob.
        blob = self.users_bucket.blob(current_user.get_id())
        json_object = blob.download_as_string()
        user_info = json.loads(json_object)
        user_info["Language"] = new_language
        # Update GCS
        with blob.open("w") as f:
            json_object = json.dumps(user_info)
            f.write(json_object)

    # TODO test
    def update_night_mode(self, new_bool):
        # Retrieve user blob.
        blob = self.users_bucket.blob(current_user.get_id())
        # Reading blob
        json_object = blob.download_as_string()
        user_info = json.loads(json_object)
        user_info["Night_Mode"] = new_bool
        # Update GCS
        with blob.open("w") as f:
            json_object = json.dumps(user_info)
            f.write(json_object)

    # TODO test
    def update_bookmarks(self, new_page):
        # Retrieve user blob.
        blob = self.users_bucket.blob(current_user.get_id())
        # Reading blob
        json_object = blob.download_as_string()
        user_info = json.loads(json_object)
        # Pass list through a set to prevent duplicate pages from being added
        temp = set(user_info["Bookmarks"])
        temp.add(new_page)
        # Turn back into list for json file
        new_list = list(temp)
        user_info["Bookmarks"] = new_list
        # Update GCS
        with blob.open("w") as f:
            json_object = json.dumps(user_info)
            f.write(json_object)

    def get_current_settings(self):
        # Retrieve user blob.
        blob = self.users_bucket.blob(current_user.get_id())
        # Reading blob
        json_object = blob.download_as_string()
        user_info = json.loads(json_object)
        user_info.pop("Password")
        return user_info

    def search(self, search_term):
        result_docs = set()
        blob = self.wiki_search_content.blob("inverted_index")
        with blob.open("r") as f:
            # Retrieving inverted index from json file in GCS
            json_index = f.read()
            inverted_index = json.loads(json_index)
            word = search_term.lower().split()
            for term in word:
                if term in inverted_index:
                    for files in inverted_index[term]:
                        file_name = files.split('/')
                        result_docs.add(file_name[-1])
            return result_docs

    def update_review(self, review, wiki_page):
        blob = self.reviews_bucket.blob(wiki_page)
        # Check if exists
        json_object = blob.download_as_string()
        if json_object:
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
        json_object = blob.download_as_string()
        # Check if exists
        if json_object:
            reviews_list = json.loads(json_object)
            sum_list = sum(reviews_list)
            average = round(sum_list / len(reviews_list), 1)
            return average
        else:
            # If no reviews exist yet
            return 0
