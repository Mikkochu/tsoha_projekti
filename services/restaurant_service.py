from app import db
from services.image_service import delete_restaurant_image


def create_restaurant(name:str, address:str, intro:str, lat:float, lng:float):
    sql = "INSERT INTO projekti.restaurants (name, address, intro, lat, lng)" \
          " VALUES (:name, :address, :intro, :lat, :lng) RETURNING id"
    result = db.session.execute(sql, {"name": name, "address": address, "intro":intro, "lat":lat, "lng":lng})
    db.session.commit()
    return result.fetchone()[0]

def get_restaurants():
    sql = "SELECT re.id as id, name, address, intro, COALESCE(ROUND(AVG(grade), 2),0.0) as avg  from projekti.restaurants as re LEFT JOIN projekti.reviews as rw ON re.id = rw.restaurant_id GROUP BY restaurant_id, re.id"
    result = db.session.execute(sql)
    return result.fetchall()


def remove_restaurant(restaurant_id:str):
    sql = f"DELETE FROM projekti.restaurants WHERE id = {restaurant_id}"
    db.session.execute(sql)
    db.session.commit()

    sql = f"DELETE FROM projekti.reviews WHERE restaurant_id = {restaurant_id}"
    db.session.execute(sql)
    db.session.commit()

    delete_restaurant_image(restaurant_id)


def get_restaurant(id:int):
    sql = "SELECT * FROM projekti.restaurants WHERE id = (:id)"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def search_restaurant(search_string):
    sql = """SELECT * FROM projekti.restaurants WHERE LOWER(name) LIKE :search_string"""
    result = db.session.execute(sql, {"search_string": f"%{search_string}%"})
    return result.fetchall()


def update_restaurant_field(field_name, value, id):
    sql = """UPDATE projekti.restaurants SET :field_name = :value WHERE id = :id"""
    sql = f"""UPDATE projekti.restaurants SET {field_name} = :value WHERE id = :id"""
    print(sql)
    db.session.execute(sql, {"value": value, "id":id})
    db.session.commit()


def check_existing_restaurants(name):
    sql = """SELECT COUNT(*) FROM projekti.restaurants AS r WHERE LOWER(r.name ) = :name"""
    result = db.session.execute(sql, {"name":name })
    count = result.fetchone()[0]
    if count >= 1:
        return True

    return False

