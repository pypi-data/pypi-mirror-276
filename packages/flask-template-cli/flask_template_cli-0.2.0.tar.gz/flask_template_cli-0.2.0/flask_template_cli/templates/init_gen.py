"""
Generate the __init__.py file for the package
"""

import os
from typing import TextIO


def init_gen(project):
    file_location = os.path.join(project.name, "app/__init__.py")
    with open(file_location, "w") as f:
        f.write(f"from flask import Flask\n\n")

        # if project.need_database:
        #     if project.db_type == "SQL":
        #         f.write("from flask_sqlalchemy import SQLAlchemy\n\n")
        #     elif project.db_type == "NoSQL":
        #         f.write("from flask_mongoengine import MongoEngine\n\n")

        f.write(f"""
def create_app(): 
    app = Flask(__name__)\n\n""")

        if project.need_database:
            f.write(f"\tfrom .models import db\n")
            f.write(f"\tdb.init_app(app)\n\n")

        _routes_import(project, f)

        _auth_import(project, f)

        f.write(f"\treturn app\n")
        f.write(f"\n")


def _routes_import(project, f: TextIO):
    if project.project_type == "api":
        f.write(f"\tfrom .routes import api\n")
        f.write(f"\tapi.init_app(app)\n")
    else:
        f.write(f"\tfrom .routes import my_routes\n")
        f.write(f"\tapp.register_blueprint(my_routes)\n\n")


def _auth_import(project, f: TextIO):
    if project.need_auth:
        f.write(f"\tfrom .routes import auth\n")
        f.write(f"\tapp.register_blueprint(auth)\n\n")

        if project.auth_type == "cookie":
            f.write(f"\tfrom .routes import login_manager\n")
            f.write(f"\tlogin_manager.init_app(app)\n\n")

        elif project.auth_type == "token":
            f.write(f"\tfrom .routes import jwt\n")
            f.write(f"\tjwt.init_app(app)\n\n")
