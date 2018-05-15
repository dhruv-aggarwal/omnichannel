# Import all Blueprints
from .api import status


def load_blueprints(current_app):
    # Register all Blueprints
    current_app.register_blueprint(status, url_prefix='/api/status')

    return current_app
