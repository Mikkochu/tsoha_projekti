import flask
import io
from flask import render_template, request, redirect, session, make_response, send_file
import services.account_service as account_service
import services.image_service as picture_service
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from forms.account_forms import PictureForm


blueprint = flask.Blueprint('home', __name__, template_folder='templates')


# ################### INDEX #################################


@blueprint.route("/", methods=["GET", "POST"])
def index():

    username_logged_in = session.get("username")
    if not username_logged_in:
        return redirect("/login")


    user = account_service.find_user_by_username(username_logged_in)
    username, is_admin = user

    if not username:
        return redirect("/login")

    user_id = account_service.find_id_by_username(username)[0]


    return render_template("home/index.html", user_id=user_id, admin=is_admin)

