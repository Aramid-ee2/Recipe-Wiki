# Imported request to be able to acces info returned from inputs
from flask import Flask,render_template, redirect, flash, request, url_for
from flask_login import login_user, login_required
from flaskr.login import User
import base64
#from flaskr.__init__ import 

def make_endpoints(app, backend,logging ):
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
        all_pages = backend.get_all_page_names()
        return render_template("pages.html", result = all_pages)
          

    # Pages Route
    @app.route("/pages/<page_id>")
    def get_page(page_id):
        page_data = backend.get_wiki_page(page_id)
        # Returns a different page depending on the page_id input
        #return render_template("welcome.html", page_data)
        return page_data

    # Sign up Route
    @app.route("/sign_up" , methods=['GET', 'POST'])
    def sign_up():
        # If the request is a Post, get username and password from the request and pass it to backend class
        if request.method == 'POST':
            backend.sign_up(request.form['user_name'], request.form['password'])
        # If the request is a Get, then return the page
        else:
            return render_template("sign_up.html")

    @app.route("/about")
    def about():
        author_image1= backend.get_image("aramide.PNG")
        author_image2= backend.get_image("gabriel.jpeg")
        
        encoded_author1 = base64.b64encode(author_image1)
        encoded_author2 = base64.b64encode(author_image2)
        #img1 = encoded_author1.decode('utf-8'), img2 = encoded_author2.decode('utf-8') )
        
        return render_template("about.html", img1 = encoded_author1.decode('utf-8'), img2 = encoded_author2.decode('utf-8'))
# Encoding image resource

    
    @app.route("/log_in", methods = ["GET", "POST"])
    def login():
        #if the request
        if request.method == 'POST':
            #Get what user puts into the form which is username and password
            user_name = request.form["user_name"]
            password  = request.form["password"]
            #Call backend.signin to check valid details
            if backend.sign_in(user_name, password):
                #Create an instance of the class user
                user = User(user_name)
                login_user(user)
                #flask.flash('Successfully logged in ')
                #Redirect users to home page after logging in
                return redirect(url_for('home'))
           
            #return render_template("welcome.html", name = user_name)
            
        return render_template("log_in.html")

    # Upload Route
    @app.route("/upload" , methods = ["GET" , "POST"])
    @login_required
    def upload():
        # Fix Post 
        if request.method == "POST":
            backend.upload(request.files['file'])
        # TODO: Redirect user to home page after uploading a file
        return render_template("upload.html")

