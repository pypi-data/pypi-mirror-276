import os


def generate_models(project):
    file_location = os.path.join(project.name, "app/models/index.py")
    if project.need_database:
        with open(file_location, "w") as f:
            if project.db_type == "SQL":
                f.write(f"from . import db\n\n")

                # f.write(f"class User(db.Model):\n")
                # f.write(f"\tid = db.Column(db.Integer, primary_key=True)\n")
                # f.write(f"\tusername = db.Column(db.String(80), unique=True, nullable=False)\n")
                # f.write(f"\temail = db.Column(db.String(120), unique=True, nullable=False)\n")
                # f.write(f"\n")
            elif project.db_type == "NoSQL":
                f.write(f"from . import db\n\n")

                # f.write(f"db = MongoEngine()\n\n")
                # f.write(f"class User(db.Document):\n")
                # f.write(f"\tusername = db.StringField(max_length=80, unique=True, required=True)\n")
                # f.write(f"\temail = db.StringField(max_length=120, unique=True, required=True)\n")
                # f.write(f"\n")

            f.write(f"\n\n# Add your models here\n")

        generate_init_file_for_models(project)

    return "Models generated successfully"


def generate_init_file_for_models(project):
    file_location = os.path.join(project.name, "app/models/__init__.py")
    if project.need_database:
        with open(file_location, "w") as f:
            if project.db_type == "SQL":
                f.write(f"from flask_sqlalchemy import SQLAlchemy\n\n")
                f.write(f"db = SQLAlchemy()\n\n")
            elif project.db_type == "NoSQL":
                f.write(f"from flask_mongoengine import MongoEngine\n\n")
                f.write(f"db = MongoEngine()\n\n")
