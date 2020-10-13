import flask
from flask import render_template, request, redirect, session, url_for, make_response, send_file, flash
import services.account_service as account_service
import services.restaurant_service as restaurant_service
import services.review_service as review_service



blueprint = flask.Blueprint('review', __name__, template_folder='templates')


@blueprint.route("/review_restaurant", methods=["GET"])
def review_restaurant_get():
    username_logged_in = session.get("username")
    user = account_service.find_user_by_username(username_logged_in)
    user_id = account_service.find_id_by_username(username_logged_in)[0]

    if user:
        username = user[0]

    if not username:
        return redirect("/")

    restaurants = restaurant_service.get_restaurants()


    return render_template("review/review_restaurant.html", restaurants=restaurants, user_id=user_id)

@blueprint.route("/review_restaurant", methods=["POST"])
def review_restaurant_post():

    _id = request.form.get("id")
    review = request.form.get("review")
    grade = request.form.get("grade")
    user_id = request.form.get("user_id")

    print(_id,review,grade, user_id)

    if not _id or not review or not grade:
        return redirect("/review_restaurant")

    reviewed_already = review_service.check_for_existing_reviews(restaraunt_id=int(_id), user_id=int(user_id))

    if reviewed_already:
        flash(f"You have already reviewed this restaurant", "danger")
        return redirect("/review_restaurant")

    review_service.review_restaurant(review=review, restaurant_id=int(_id), grade=int(grade), user_id=int(user_id))

    return redirect("/review_restaurant")

@blueprint.route("/delete_review", methods=["POST"])
def delete_review_from_user_page():
    review_id = request.form.get("review_id")
    user_id = request.form.get("user_id") # ei tarvita varmaan
    review_service.delete_review_by_review_id(review_id)

    return redirect(f"/user/{user_id}")
