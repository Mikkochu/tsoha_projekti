from app import db


def review_restaurant(review: str, restaurant_id: int, grade: int, user_id: int):
    sql = "INSERT INTO projekti.reviews (review, restaurant_id, grade, user_id) VALUES (:review, :restaurant_id, :grade, :user_id)"
    db.session.execute(sql, {"review": review, "restaurant_id": restaurant_id, "grade": grade, "user_id": user_id})
    db.session.commit()


def get_review_by_user_id(user_id: int):
    sql = f"SELECT re.name, rw.review, rw.grade, rw.id FROM projekti.reviews as rw " \
          f"JOIN projekti.restaurants as re ON rw.restaurant_id = re.id WHERE rw.user_id = :user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def get_reviews_by_restaurant_id(restaurant_id: int):
    sql = """SELECT rw.review, rw.grade, rw.user_id FROM projekti.reviews AS rw
             JOIN projekti.users AS u ON rw.user_id = u.id
             WHERE rw.restaurant_id = :restaurant_id"""
    result = db.session.execute(sql, {"restaurant_id": restaurant_id})
    return result.fetchall()

def delete_review_by_review_id(review_id):
    sql = f"""DELETE FROM projekti.reviews WHERE id = :id """
    db.session.execute(sql, {"id":review_id})
    db.session.commit()

def check_for_existing_reviews(restaraunt_id, user_id):
    sql = """SELECT COUNT(*) FROM projekti.reviews as rw WHERE rw.restaraunt_id = :restaraunt_id AND rw.user_id = :user_id"""
    sql = """SELECT COUNT(*) FROM projekti.reviews AS rw WHERE rw.restaurant_id = :restaraunt_id AND rw.user_id = :user_id"""
    result = db.session.execute(sql, {"restaraunt_id": restaraunt_id,"user_id": user_id})
    count = result.fetchone()[0]
    if count >= 1:
        return True

    return False
