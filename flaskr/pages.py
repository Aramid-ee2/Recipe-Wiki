from flask import render_template, request
def make_endpoints(app, backend,logging):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def main():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the main page.
        logging.info("Someone hit the Main Page")
        return render_template("main.html")
    # Home Page Route
    @app.route("/home")
    def home():
        return render_template("home.html")        
    # Pages Route
    @app.route("/pages/<page_id>")
    def get_page(page_id):
        return render_template("{}.html".format(page_id))

    # Sign up
    @app.route("/sign_up" , methods=['GET', 'POST'])
    def sign_up():
        # If the request is a Get, then return the page
        # If the request is a Post, get username and password from the request and pass it to backend class
        if request.method == 'POST':
            backend.sign_up(request.form['user_name'], request.form['password'])
        else:
            return render_template("sign_up.html")
