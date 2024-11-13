import os
import logging
import uuid
from flask import Flask,g, request
from flask_caching import Cache
from dotenv import load_dotenv

from .db import db, get_connection_string
from .errors import register_errors

load_dotenv()

def set_log_level(app):
    DEFAULT_LOG_LEVEL = 'WARNING'

    if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    else:
        app.logger.setLevel(os.getenv('LOG_LEVEL', DEFAULT_LOG_LEVEL))

    return app

def configure(app):
    # Set up caching configuration
    app.config['CACHE_TYPE'] = 'simple'  # or 'filesystem', 'redis', 'memcached', etc.
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Optional: set default cache timeout (in seconds)

    # SQLAlchemy pool configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 10         # Number of connections to keep in the pool
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5      # Timeout in seconds to get a connection from the pool
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600    # Time in seconds to recycle a connection
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20      # Number of connections to allow beyond the pool size

def add_request_id(app):
    # Generate a request ID for each incoming request
    @app.before_request
    def generate_request_id():
        g.request_id = str(uuid.uuid4())
        app.logger.info(f"Request ID: {g.request_id} - {request.method} {request.path}")

    # Custom log format including the request ID
    @app.after_request
    def add_request_id_to_log(response):
        app.logger.info(f"Request ID: {g.request_id} finished")
        return response

def create_app():
    app = Flask(__name__)



    app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
    set_log_level(app)
    add_request_id(app)

    # ----------------------------------------
    # Debugging log level
    # ----------------------------------------
    current_log_level = app.logger.getEffectiveLevel()
    log_level_name = logging.getLevelName(current_log_level)
    app.logger.info(f"Current log level: {log_level_name}")

    configure(app)

    # Validations before running the app go here

    # Must be done after setting up the configuration
    cache = Cache(app)

    db.init_app(app)
    if os.getenv('FLASK_ENV') == 'development':
        from flask_migrate import Migrate
        migrate = Migrate(app, db)

    with app.app_context():
        app.cache = cache

        from .routes import home
        from .routes import activities

        # Register Blueprints
        app.register_blueprint(home.bp)
        app.register_blueprint(activities.bp, url_prefix='/activities')

        register_errors(app)

        return app
