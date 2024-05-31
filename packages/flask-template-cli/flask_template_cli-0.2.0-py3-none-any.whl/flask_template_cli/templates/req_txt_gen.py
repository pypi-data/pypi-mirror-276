"""
Generate requirements.txt file
"""


def req_txt_gen(project):
    file_location = f"{project.name}/requirements.txt"

    with open(file_location, "w") as file:
        project.add_requirements("flask")

        if project.project_type == "api":
            # Add flask-restful if project type is API
            project.add_requirements("flask-restful")

        if project.need_database:
            # Add database requirements
            _database_requirements(project)

        # Write requirements to file
        file.write("\n".join(project.requirements))


def _database_requirements(project):
    if project.need_database:
        if project.db_type == "SQL":
            project.add_requirements("sqlalchemy")
            if project.db_engine == "Postgres":
                # Add psycopg2-binary if database engine is Postgres
                project.add_requirements("psycopg2-binary")
            elif project.db_engine == "MySQL":
                # Add mysql-connector-python if database engine is MySQL
                project.add_requirements("mysql-connector-python")
        elif project.db_type == "NoSQL":
            # Add mongoengine if database type is NoSQL and engine is MongoDB
            project.add_requirements("mongoengine") if project.db_engine == "MongoDB" else None
