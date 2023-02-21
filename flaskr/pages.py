from flask import render_template


def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html")
    # Pages
    @app.route("/Chicken_Tamales")
    def Chicken_Tamales():
        return render_template("Chicken_Tamales.html")
    @app.route("/Green_Chicken_Enchiladas")
    def Green_Chicken_Enchiladas():
        return render_template("Green_Chicken_Enchiladas.html")
    @app.route("/Huevos_Rancheros")
    def Huevos_Rancheros():
        return render_template("Huevos_Rancheros.html")
    @app.route("/Molletes")
    def Molletes():
        return render_template("Molletes.html")
    # End Pages

    # Sign up
    @app.route("/sign_up")
    def sign_up():
        return render_template("sign_up.html")
        # If the request is a Get, then return the page
        # If the request is a Post, get username and password from the request and pass it to backend class
