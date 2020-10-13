from app import  db
from werkzeug.security import check_password_hash, generate_password_hash
from typing import Optional



def login_service(username:str):
    sql = "SELECT password FROM projekti.users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    password = result.fetchone()
    return password


def register_service(username:str, hash_value:str):
    sql = "INSERT INTO projekti.users (username, password) VALUES (:username,:password)"
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()

def check_existing_user(username:str) -> bool:
    sql = "SELECT username FROM projekti.users WHERE username = :username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user != None:
        return False
    return True

def find_user_by_username(username:str):
    sql = "SELECT username, auth FROM projekti.users WHERE username = :username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user


def find_id_by_username(username:str):
    sql = "SELECT id FROM projekti.users WHERE username = :username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user


def delete_user(user_id:int):
    sql = "DELETE FROM projekti.users WHERE id = :id"
    db.session.execute(sql, {"id": user_id})

    sql = "DELETE FROM projekti.user_images WHERE user_id = :id"
    db.session.execute(sql, {"id": user_id})

    db.session.commit()

def delete_user_image(user_id):
    sql = "DELETE FROM projekti.user_images WHERE user_id = :id"
    db.session.execute(sql, {"id": user_id})
    db.session.commit()


