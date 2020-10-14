from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask_googlemaps import GoogleMaps


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)
GoogleMaps(app, key=getenv("GOOGLE_API_KEY"))


def main():
    register_blueprints()
    app.run()


def register_blueprints():
    from routes import home_routes
    from routes import account_routes
    from routes import restaraunt_routes
    from routes import review_routes
    app.register_blueprint(home_routes.blueprint)
    app.register_blueprint(account_routes.blueprint)
    app.register_blueprint(restaraunt_routes.blueprint)
    app.register_blueprint(review_routes.blueprint)



if __name__ == "__main__":
    main()

