def gen_auth_files(project):
    file_location = f"{project.name}/app/routes/auth.py"
    with open(file_location, "w") as f:
        if project.need_auth:
            if project.auth_type == "cookie":
                project.add_requirements("flask-login")
                f.write(_gen_auth_routes_cookie())

            if project.auth_type == "token":
                project.add_requirements("flask-jwt-extended")
                f.write(_gen_auth_routes_token())


def _gen_auth_routes_cookie():
    return """

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    # implement login logic here
    pass 

@auth.route('/register', methods=['POST'])
def register():
    # implement register logic here
    pass


@auth.route('/logout')
@login_required
def logout():
    # implement logout logic here
    pass

"""


def _gen_auth_routes_token():
    return """
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    # implement login logic here with JWT access token
    pass

@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    # implement refresh token logic here
    pass


# @auth.route('/blacklist', methods=['POST'])
# @jwt_required
# def blacklist_token():
    # implement token blacklist logic here
#     pass



@auth.route('/register', methods=['POST'])
def register():
    # implement register logic here
    pass

@auth.route('/logout')
@jwt_required
def logout():
    # implement logout logic here
    pass
    
"""
