from flask import Flask
from connexion import FlaskApp
from os import makedirs

def create_app(test_config=None):
    """Constructs the core application."""
    # app = Flask(__name__, instance_relative_config=True)
    # Create app that loads Swagger (OpenAPI) API specs
    app = FlaskApp(__name__, specification_dir='openapi/')
    # app.add_api('auth.yaml', base_path='/auth', strict_validation=True)
    app.add_api('auth.yaml', base_path='/auth')
    # app.add_api('restaurants.yaml')
    
    # Load instance config:
    if test_config is None:
        app.app.config.from_object('config.Config')
    else:
        app.app.config.from_mapping(test_config)
    
    # Ensure instance folder exists:
    try:
        makedirs(app.app.instance_path)
    except OSError:
        pass
    
    from . import auth
    app.app.register_blueprint(auth.bp)
    
    from . import sb
    sb.init_app(app.app)
    
    # from . import gmaps
    # gmaps.init_app(app)
    
    # from . import restaurant
    # app.register_blueprint(restaurant.bp)
    # app.add_url_rule('/', endpoint='index')
    
    return app.app
    
    