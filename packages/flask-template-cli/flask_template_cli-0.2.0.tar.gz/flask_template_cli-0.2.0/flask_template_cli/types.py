class Project:
    def __init__(self):
        self._name = None
        self._project_type = None
        self._need_database = False
        self._db_type = None
        self._db_engine = None
        self._requirements = []
        self._need_auth = False
        self._auth_type = None

    @property
    def name(self):
        return self._name

    @property
    def project_type(self):
        return self._project_type

    @property
    def need_database(self):
        return self._need_database

    @property
    def db_engine(self):
        return self._db_engine

    @property
    def db_type(self):
        return self._db_type

    @property
    def requirements(self):
        return self._requirements

    @property
    def auth_type(self):
        return self._auth_type

    @property
    def need_auth(self):
        return self._need_auth

    @name.setter
    def name(self, value):
        self._name = value

    @project_type.setter
    def project_type(self, value):
        self._project_type = value

    @need_database.setter
    def need_database(self, value):
        self._need_database = value

    @db_engine.setter
    def db_engine(self, value):
        self._db_engine = value

    @db_type.setter
    def db_type(self, value):
        self._db_type = value

    @need_auth.setter
    def need_auth(self, value):
        self._need_auth = value

    @auth_type.setter
    def auth_type(self, value):
        self._auth_type = value

    def add_requirements(self, value):
        self._requirements.append(value)
