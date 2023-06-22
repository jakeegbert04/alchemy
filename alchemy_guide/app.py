#app.py

from flask import Flask, request, jsonify
from db import *
import os
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from users import Users
from organizations import Organizations

database_pre = os.environ.get("DATABASE_PRE")
database_addr = os.environ.get("DATABASE_ADDR")
database_user = os.environ.get("DATABASE_USER")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_user}@{database_addr}:{database_port}/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)


def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("All Done")


@app.route('/user/add', methods=["POST"])
def add_user():
    req_data = request.form if request.form else request.json

    fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'state', 'org_id', 'active']
    req_fields = ['name', 'email', 'org_id']

    values = {}

    for field in fields:
        field_data = req_data.get(field)
        if field_data in req_fields and not field_data:
            return jsonify(f'{field} is required'), 400

        values[field] = field_data

    new_user = Users(
        values['first_name'],
        values['last_name'],
        values['email'],
        values['phone'],
        values['city'],
        values['state'],
        values['org_id'],
        values['active'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify('User Created'), 200


@app.route('/user/update/<id>', methods=["PUT"])
def user_update(id):

    req_data = request.form if request.form else request.json

    user = Users.query.get(id)

    if not user:
        return jsonify("User not found"), 404

    fields_to_update = ['first_name', 'last_name', 'email', 'phone', 'city', 'state', 'org_id', 'active']

    for field in fields_to_update:
        if field in req_data:
            setattr(user, field, req_data[field])

    db.session.commit()

    return jsonify("User updated"), 200


@app.route('/users/get', methods=['GET'])
def get_all_active_users():
    users = db.session.query(Users).filter(Users.active == True).all()

    users_list = []

    for user in users:
        user_dict = {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "city": user.city,
            "state": user.state,
            "organization": {
                "org_id": user.organization.org_id,
                "name": user.organization.name,
                "phone": user.organization.phone,
                "city": user.organization.city,
                "state": user.organization.state,
                "active": user.organization.active,
            },

            "active": user.active,
        }

        users_list.append(user_dict)
    return jsonify(users_list), 200


@app.route("/user/get/<id>", methods=["GET"])
def get_users_by_id(id):
    user = db.session.query(Users).filter(Users.user_id == id).first()

    if not user:
        return jsonify("That user doesn't exit"), 404

    user_dict = {
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "city": user.city,
        "state": user.state,
        "organization": {
            "org_id": user.organization.org_id,
            "name": user.organization.name,
            "phone": user.organization.phone,
            "city": user.organization.city,
            "state": user.organization.state,
            "active": user.organization.active,
        },
        "active": user.active,
    }

    return jsonify(user_dict), 200

@app.route('/user/status/<id>', methods=["PATCH"])
def user_status(id):
     user = db.session.query(Users).filter(Users.user_id == id).first()

     if user:
          user.active = not user.active
          db.session.commit()
          return jsonify(f"User status set to: {user.active}"), 203
     else:
          return jsonify("User not found"), 404

@app.route('/user/delete/<id>', methods=["DELETE"])
def user_delete(id):

    user = Users.query.get(id)

    if not user:
        return jsonify('User not found'), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify('User deleted'), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(f'Error deleting user: {str(e)}'), 500




@app.route('/orgs/add', methods=["POST"])
def add_organization():
    req_data = request.form if request.form else request.json

    fields = ['name', 'phone', 'city', 'state', 'active']
    req_fields = ['name']

    values = {}

    for field in fields:
        field_data = req_data.get(field)
        if field_data in req_fields and not field_data:
            return jsonify(f'{field} is required'), 400

        values[field] = field_data

    new_org = Organizations(values['name'], values['city'], values['state'], values['phone'], values['active'])
    db.session.add(new_org)
    db.session.commit()

    return jsonify('Organization Created'), 200

@app.route('/org/update/<id>', methods=["PUT"])
def org_update(id):

    req_data = request.form if request.form else request.json

    organization = Organizations.query.get(id)

    if not organization:
        return jsonify("Organization not found"), 404

    fields_to_update = ['name', 'last_name', 'city', 'state', 'phone', 'active']

    for field in fields_to_update:
        if field in req_data:
            setattr(organization, field, req_data[field])

    db.session.commit()

    return jsonify("Organization updated"), 200



@app.route('/orgs/get', methods=['GET'])
def get_all_active_orgs():
    organizations = db.session.query(Organizations).filter(Organizations.active == True).all()

    orgs_list = []

    for organization in organizations:
        org_dict = {
            "org_id": organization.org_id,
            "name": organization.name,
            "phone": organization.phone,
            "city": organization.city,
            "state": organization.state,
            "active": organization.active,
        }

        orgs_list.append(org_dict)
    return jsonify(orgs_list), 200

@app.route("/org/get/<id>", methods=["GET"])
def get_org_by_id(id):
    org_record = db.session.query(Organizations).filter(Organizations.org_id == id).first()

    if not org_record:
        return jsonify("That organization doesn't exit"), 404

    org_record_dict = {
        "org_id": org_record.org_id,
        "name": org_record.name,
        "phone": org_record.phone,
        "city": org_record.city,
        "state": org_record.state,
        "active": org_record.active,
    }

    return jsonify(org_record_dict), 200

@app.route('/org/status/<id>', methods=["PATCH"])
def org_status(id):
     org = db.session.query(Organizations).filter(Organizations.org_id == id).first()

     if org:
          org.active = not org.active
          db.session.commit()
          return jsonify(f"Organization status set to: {org.active}"), 203
     else:
          return jsonify("Organization not found"), 404

@app.route('/org/delete/<id>', methods=["DELETE"])
def org_delete(id):
    print(f"Deleting organization with ID: {id}")

    organization = Organizations.query.get(id)

    if not organization:
        return jsonify('Organization not found'), 404

    try:
        db.session.delete(organization)
        db.session.commit()
        return jsonify('Organization deleted'), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify('Cannot delete organization with associated users'), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(f'Error deleting organization: {str(e)}'), 500

if __name__ == "__main__":
    create_all()
    app.run(port=8089, host="0.0.0.0", debug=True)