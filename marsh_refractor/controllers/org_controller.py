# CREATE
from flask import request, jsonify
from models.organizations import Organizations, organization_schema, organizations_schema
from db import db
from util.reflection import populate_object

def add_organization():
    req_data = request.form if request.form else request.json

    if not req_data:
        return jsonify("Please enter all fields")
    
    new_org = Organizations.new_org()

    populate_object(new_org, req_data)

    db.session.add(new_org)
    db.session.commit()

    return jsonify('Organization Created'), 200
#READ
def get_org_by_id(id):
    org_record = db.session.query(Organizations).filter(Organizations.org_id == id).first()

    if not org_record:
        return jsonify("That organization doesn't exit"), 404
    else:
        return jsonify(organization_schema.dump(org_record)), 200

def get_all_orgs():
    orgs = db.session.query(Organizations).all()
    if not orgs:
        return jsonify("There are no Orgs"), 404
    else:
        return jsonify(organizations_schema.dump(orgs)), 200

#UPDATE

#ACTIVATE/DEACTIVATE

#DELETE