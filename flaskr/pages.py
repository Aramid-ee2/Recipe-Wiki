# Imported request to be able to acces info returned from inputs
from flask import Flask, render_template, redirect, flash, request, url_for, Response
from flask_login import login_user, login_required, logout_user, current_user
from flaskr.login import User

import base64


def make_endpoints(app, backend, logging):
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    # Default route
    @app.route("/")
    def main():
        # TODO: Log test
        logging.info("Someone hit the Main Page")
        return render_template("main.html")

    # Home Page Route
    @app.route("/home")
    def home():
        return render_template("home.html")

    @app.route("/pages")
    def pages():
        #call get_all_page_names from backend to get the list of all the page names in google cloud storage
        all_pages = backend.get_all_page_names(current_user)
        #return the list of all page names to html inorder for it to be displayed
        return render_template("pages.html", result=all_pages)

    # Pages Route
    @app.route("/pages/<page_id>")
    def get_page(page_id):
        #call get_wiki_page from backend to get the respective page data depending on page_id
        page_data = backend.get_wiki_page(page_id, current_user)
        return render_template('wiki_page.html', page_data=page_data)

    # TODO test route
    @app.route("/pages/<page_id>")
    def bookmark_page(page_id):
        backend.update_bookmarks(page_id)
        #call get_wiki_page from backend to get the respective page data depending on page_id
        page_data = backend.get_wiki_page(page_id)

        return render_template('wiki_page.html', page_data=page_data)

    # Sign up Route
    @app.route("/sign_up", methods=['GET', 'POST'])
    def sign_up():
        # If the request is a Post, get username and password from the request and pass it to backend class
        if request.method == 'POST':
            backend.sign_up(request.form['user_name'], request.form['password'])
            return render_template("log_in.html")
        # If the request is a Get, then return the page
        else:
            return render_template("sign_up.html")

    @app.route("/about")
    def about():
        #call the backend get_image on each image
        author_image1 = backend.get_image("aramide.PNG")
        author_image2 = backend.get_image("gabriel.jpeg")
        author_image3 = backend.get_image("julian.PNG")

        encoded_author1 = base64.b64encode(author_image1)
        encoded_author2 = base64.b64encode(author_image2)
        encoded_author3 = base64.b64encode(author_image3)
        #encoding the image binary data

        return render_template("about.html",
                               img1=encoded_author1.decode('utf-8'),
                               img2=encoded_author2.decode('utf-8'),
                               img3=encoded_author3.decode('utf-8'))
        #creating a string of unicode characters using "utf-8" encoding , sending the unicoded characters to the html file

    @app.route("/log_in", methods=["GET", "POST"])
    def login():
        #if the request is a post
        if request.method == 'POST':
            #Get what user puts into the form which is username and password
            user_name = request.form["user_name"]
            password = request.form["password"]
            #Call backend.signin to check valid details
            if backend.sign_in(user_name, password):
                #Create an instance of the class user
                current_user = User(user_name)
                login_user(current_user)
                #log the user in

                #Redirect users to home page after successfully logging in
                return redirect(url_for("home"))

        return render_template("log_in.html")

    # Upload Route
    @app.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload():
        # Fix Post
        if request.method == "POST":
            backend.upload(request.files['file'])
        # Redirect user to home page after uploading a file
        return render_template("upload.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/home")

    # Settings Route
    #TODO: Test route
    @app.route("/settings")
    def settings():
        settings = backend.get_current_settings()
        return render_template("settings.html", settings=settings)

    #TODO: Test route
    @app.route("/settings/language", methods=["POST"])
    def settings_language():
        # Update language
        backend.update_language(request.form["fav_language"])
        settings = backend.get_current_settings()
        return render_template("settings.html", settings=settings)

   