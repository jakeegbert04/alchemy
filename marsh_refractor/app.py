from flask import Flask, request, jsonify
from db import *
import os
from flask_marshmallow import Marshmallow
from routes.org_routes import org
from routes.user_routes import user

from models.users import Users, user_schema, users_schema
from models.organizations import Organizations, organizations_schema, organization_schema
from util.reflection import populate_object

database_pre = os.environ.get("DATABASE_PRE")
database_addr = os.environ.get("DATABASE_ADDR")
database_user = os.environ.get("DATABASE_USER")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_user}@{database_addr}:{database_port}/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app)

app.register_blueprint(org)
app.register_blueprint(user)

def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("All Done")

if __name__ == "__main__":
    create_all()
    app.run(port=8089, host="0.0.0.0", debug=True)