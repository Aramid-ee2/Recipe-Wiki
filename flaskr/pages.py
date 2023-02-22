from flask import render_template


def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html")
    # Pages Route
    @app.route("/pages/<page_id>")
    def get_page(page_id):
        return render_template("{}.html".format(page_id))

    # Sign up
    @app.route("/sign_up")
    def sign_up():
        return render_template("sign_up.html")
        # If the request is a Get, then return the page
        # If the request is a Post, get username and password from the request and pass it to backend class
