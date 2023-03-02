# Imported request to be able to acces info returned from inputs
from flask import render_template, request
def make_endpoints(app, backend,logging):
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
            pass
        # If the request is a Get, return upload page
        else:
            return render_template("upload.html")
