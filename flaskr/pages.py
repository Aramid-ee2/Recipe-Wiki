# Imported request to be able to acces info returned from inputs
from flask import Flask, render_template, request, url_for, session
from flaskr.login import User

def make_endpoints(app, backend,logging, ):
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
    # Pages Route
    @app.route("/pages/<page_id>")
    def get_page(page_id):
        # Returns a different page depending on the page_id input
        return render_template("{}.html".format(page_id))
    # Sign up Route
    @app.route("/sign_up" , methods=['GET', 'POST'])
    def sign_up():
        # If the request is a Post, get username and password from the request and pass it to backend class
        if request.method == 'POST':
            backend.sign_up(request.form['user_name'], request.form['password'])
        # If the request is a Get, then return the page
        else:
            return render_template("sign_up.html")
    # Upload Route
    @app.route("/upload" , methods = ["GET" , "POST"])
    def upload():
        # Fix Post 
        if request.method == "POST":
            backend.upload(request.files['file'])
        # Redirect user to home page after uploading a file
        return render_template("upload.html")
    # About Route
    @app.route('/about')
    def about():
        authors = [
        {"Aramide Ogundiran":"Author 1", "image": "aramide.jpg"},
        {"Gabriel Terrazas": "Author 2","image": "gabe.jpg"},
        {"Julian Pacheco": "Author 3","image": "julian.jpg"}
        ]
        for author in authors:
            author["image_url"] = backend.get_image(author["image"])
        return render_template("about.html", authors=authors)
    @app.route('/logout')
    def logout():
        if 'username' in session:
            session.pop('username')
        return redirect('/')
    
    @app.route("/pages")
    def pages():
        pass

    
    @app.route("/log_in", methods = ["GET", "POST"])
    def login():
    #Get what user puts into the form which is username and password
    #Call backend.signin to check valid details
    #Create an instance of the class user
    #Login_user(user)
    #render the html
        pass

