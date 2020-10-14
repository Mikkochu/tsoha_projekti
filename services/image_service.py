from app import  db


def add_restaurant_image(restaurant_id, data):
    delete_restaurant_image(restaurant_id)
    sql = "INSERT INTO restaurant_images (restaurant_id, data) VALUES (:restaurant_id,:data)"
    db.session.execute(sql, {"restaurant_id":restaurant_id, "data":data})
    db.session.commit()


def delete_restaurant_image(restaurant_id):
    sql = """DELETE FROM restaurant_images WHERE restaurant_id = :restaurant_id"""
    db.session.execute(sql, {"restaurant_id":restaurant_id})
    db.session.commit()


def get_restaurant_image(restaurant_id):
    sql = "SELECT data FROM restaurant_images WHERE restaurant_id=:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    data = result.fetchone()[0]
    return data