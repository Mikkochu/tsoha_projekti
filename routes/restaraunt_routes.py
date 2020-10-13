import flask
from flask import render_template, request, redirect, session, url_for, make_response, send_file, flash
import services.account_service as account_service
import services.image_service
import services.restaurant_service as restaurant_service
import services.review_service as review_service

blueprint = flask.Blueprint('restaurant', __name__, template_folder='templates')


# ################### INDEX #################################


@blueprint.route("/add_restaurant", methods=["GET"])
def add_restaurant_get():
    username_logged_in = session.get("username")

    if not username_logged_in:
        return redirect("/login")

    user = account_service.find_user_by_username(username_logged_in)
    username, admin = user

    if not admin:
        return redirect("/")

    user_id = account_service.find_id_by_username(username)[0]

    restaurants = restaurant_service.get_restaurants()

    return render_template("restaurant/add_restaurant.html", restaurants=restaurants, user_id=user_id)


@blueprint.route("/add_restaurant", methods=["POST"])
def add_restaurant_post():
    username_logged_in = session.get("username")
    user = account_service.find_user_by_username(username_logged_in)
    username, admin = user

    if not admin:
        return redirect("/")

    name = request.form.get("name")
    address = request.form.get("address")
    intro = request.form.get("intro")
    lat = request.form.get("lat")
    lng = request.form.get("lng")
    file = request.files['inputFile']
    data = None

    if file:
        data = file.read()

    if not name or not address:
        flash(f"Name and address are required", "danger")
        return redirect("/add_restaurant")

    existing_restaurant = restaurant_service.check_existing_restaurants(name=name)
    if existing_restaurant:
        flash(f"Restaurant already exists in database", "danger")
        return redirect("/add_restaurant")


    if not intro:
        intro = f"{name}. Tervetuloa!"

    if not lat or lng:
        lat = 00.000
        lng = 00.000


    restaurant_id = restaurant_service.create_restaurant(name=name, address=address, intro=intro, lat=lat, lng=lng)

    if file:
        services.image_service.add_restaurant_image(restaurant_id=restaurant_id, data=data)

    return redirect("/add_restaurant")


@blueprint.route("/show_restaurant_image/<int:restaurant_id>", methods=["GET"])
def show_profile_picture(restaurant_id):
    data = services.image_service.get_restaurant_image(restaurant_id=restaurant_id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response


@blueprint.route("/remove_restaurant", methods=["POST"])
def remove_restaurant_post():
    _id = request.form.get("id")
    restaurant_service.remove_restaurant(_id)
    return redirect("/add_restaurant")


@blueprint.route("/restaurant/<int:id>", methods=["GET"])
def restaurant_get(id: int):
    user_id, admin = check_user()  # todo laita kaikkiin

    restaurant = restaurant_service.get_restaurant(id)
    reviews = review_service.get_reviews_by_restaurant_id(id)

    return render_template("restaurant/restaurant.html", restaurant=restaurant, reviews=reviews, user_id=user_id)


@blueprint.route("/restaurants", methods=["GET"])
def show_restaurants():
    restaurants = restaurant_service.get_restaurants()

    username = session.get("username")
    user_id = account_service.find_id_by_username(username)[0]

    return render_template("restaurant/show_restaurants.html", restaurants=restaurants, user_id=user_id)


@blueprint.route("/search_restaraunts", methods=["POST"])
def search_restaraunts():
    user_id, admin = check_user()

    search_string = request.form.get("search")

    if search_string != '':
        search_results = restaurant_service.search_restaurant(search_string)
    else:
        search_results = None

    return render_template("restaurant/search_results.html", search_results=search_results, user_id=user_id)


@blueprint.route("/edit_restaurant/<int:id>", methods=["GET"])
def edit_restaurant_get(id):
    user_id, admin = check_user()

    if not admin:
        return redirect("/")

    restaurant_to_edit = restaurant_service.get_restaurant(id=id)

    return render_template("restaurant/edit_restaurant.html", restaurant=restaurant_to_edit, user_id=user_id)


@blueprint.route("/edit_restaurant/<int:id>", methods=["POST"])
def edit_restaurant_post(id):
    user_id, admin = check_user()

    if not admin:
        return redirect("/")


    for k, v in request.form.items():
        if not v:
            continue
        restaurant_service.update_restaurant_field(field_name=k, value=v, id=id)

    file = request.files['inputFile']
    if file:
        data = file.read()
        services.image_service.add_restaurant_image(restaurant_id=id, data=data)

    return redirect(f"/edit_restaurant/{id}")


@blueprint.route("/edit_restaurant", methods=["POST"])
def edit_restaurant_reroute():
    user_id, admin = check_user()

    if not admin:
        return redirect("/")

    restaurant_number = request.form.get("id")
    return redirect(f"/edit_restaurant/{restaurant_number}")


def check_user():  # todo siirra accounttiin ja mieti koko kuvio viela
    username_logged_in = session.get("username")
    if not username_logged_in:
        return redirect("/login")

    user = account_service.find_user_by_username(username_logged_in)
    username, is_admin = user

    user_id = account_service.find_id_by_username(username)[0]
    return user_id, is_admin
