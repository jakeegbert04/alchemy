# CREATE
from flask import request, jsonify

from db import db
from models.users import user_schema, users_schema, Users
from util.reflection import populate_object
def add_user():
    req_data = request.form if request.form else request.json

    if not req_data:
        return jsonify("Please enter all required fields")

    new_user = Users.new_user()

    populate_object(new_user, req_data)
    db.session.add(new_user)
    db.session.commit()

    return jsonify('User Created'), 200

#READ
def get_all_active_users():
    users = db.session.query(Users).filter(Users.active == True).all()

    if not users:
        return jsonify('No Users Exist'), 404
    else:
        return jsonify(users_schema.dump(users)), 200

def get_users_by_id(id):
    user = db.session.query(Users).filter(Users.user_id == id).first()

    if not user:
        return jsonify("That user doesn't exit"), 404

    else:
        return jsonify(user_schema.dump(user)), 200
#UPDATE
def update_user(id):
    req_data = request.form if request.form else request.json
    existing_user = db.session.query(Users).filter(Users.user_id == id).first()

    populate_object(existing_user, req_data)

    db.session.commit()

    return jsonify('User Created'), 200
#DEACTIVATE/ACTIVATE

#DELETE