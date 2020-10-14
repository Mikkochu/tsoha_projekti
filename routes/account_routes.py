import flask
from flask import render_template, request, redirect, session, url_for, make_response, send_file, flash
import services.account_service as account_service
import services.restaurant_service as restaurant_service
import services.review_service as review_service
from werkzeug.security import check_password_hash, generate_password_hash
from forms.account_forms import LoginForm,RegisterForm

blueprint = flask.Blueprint('account', __name__, template_folder='templates')
username = None


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    #print(username, password)
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data

        user = account_service.login_service(username)

        if user == None:
            flash(f"No such user", "danger")
            return render_template("account/login.html", form=form, title="Login")
        else:
            hash_value = user[0]
            if check_password_hash(hash_value, password):
                flash(f"Login successful for user {form.username.data}", "success")


                session["username"] = username

                return redirect("/")
            else:
                flash(f"Wrong password, go fuck yourself", "danger")
                return render_template("account/login.html", form=form, title="Login")


    return render_template('account/login.html', form=form, title="Login")



@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm = form.confirm_password.data
        #print(username, password, confirm)

        hash_value = generate_password_hash(password)
        user_exists = account_service.check_existing_user(username)

        if not user_exists:
            flash(f"Username {username} already exists. Please choose a different username", "danger")
            return render_template("account/register.html", form=form, title="Register")

        account_service.register_service(username, hash_value)
        flash(f"Account created for user {username}", "success")
        return redirect("/login")

    return render_template("account/register.html", form=form, title="Register")

@blueprint.route("/logout")
def logout():
    try:
        del session["username"]
    except KeyError:
        pass

    return redirect("/login")

@blueprint.route("/user/<int:id>", methods=["GET", "POST"])
def user(id:int):
    username = session.get("username")

    if not username:
        return redirect("/login")

    user_id = account_service.find_id_by_username(username)[0]

    if user_id != id:
        return redirect("/")

    my_reviews = review_service.get_review_by_user_id(user_id)

    return render_template("account/user.html", title="User", user_id=id, my_reviews=my_reviews)



@blueprint.route("/show_profile_picture/<int:user_id>", methods=["GET"])
def show_profile_picture(user_id):
    from app import db
    sql = "SELECT data FROM projekti.user_images WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type","image/jpeg")
    return response



@blueprint.route("/send_profile_picture", methods=["POST"])
def send_profile_picture():
    username = session.get("username")

    if not username:
        return redirect("/login")

    user_id = account_service.find_id_by_username(username)[0]

    file = request.files['inputFile']
    name = file.filename
    # if not name.endswith(".jpg"): # Voi olla myos png
    #     return "Invalid filename" #todo korjaa myos png jpeg
    data = file.read()
    if len(data) > 100*1024:
        return "Too big file"

    from app import db

    account_service.delete_user_image(user_id)
    sql = "INSERT INTO projekti.user_images (user_id, data) VALUES (:user_id,:data)"
    db.session.execute(sql, {"user_id":user_id, "data":data})
    db.session.commit()

    return redirect(f"/user/{user_id}")

@blueprint.route("/delete_image", methods=["POST"])
def delete_image_for_user():
    _id = request.form['id']
    username = session.get("username")
    user_id = account_service.find_id_by_username(username)[0]
    account_service.delete_user_image(user_id)
    return redirect(f"/user/{user_id}")

@blueprint.route("/delete_user", methods=["POST"])
def delete_user():
    _id = request.form['id']
    print(_id)
    username = session.get("username")
    user_id = account_service.find_id_by_username(username)[0]
    account_service.delete_user(user_id)

    return redirect("/login")

@blueprint.route("/admin", methods=["GET"])
def show_admin_page():
    user_id, admin = check_user()

    if not admin:
        return redirect("/")

    from services import restaurant_service
    restaurants = restaurant_service.get_restaurants()

    return render_template("account/admin.html", restaurants=restaurants, user_id=user_id)


def check_user(): #todo siirra accounttiin ja mieti koko kuvio viela
    username_logged_in = session.get("username")
    user = account_service.find_user_by_username(username_logged_in)
    username, is_admin = user

    user_id = account_service.find_id_by_username(username)[0]
    return user_id, is_admin