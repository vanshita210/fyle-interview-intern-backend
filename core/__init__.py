from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/school_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# this is to enforce fk (not done by default in sqlite3)
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# Import blueprints after creating app and db
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources
from core.apis.principal.principal import principal_api  # Import the principal_api blueprint from teachers folder

# Register blueprints
app.register_blueprint(student_assignments_resources)
app.register_blueprint(teacher_assignments_resources)
app.register_blueprint(principal_api)  # Register the principal_api blueprint

# Function to create the app (used for testing)
def create_app():
    return app
