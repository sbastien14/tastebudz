from flask import Flask
from os import makedirs

def create_app(test_config=None):
    """Constructs the core application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Load instance config:
    if test_config is None:
        app.config.from_object('config.Config')
    else:
        app.config.from_mapping(test_config)
    
    # Ensure instance folder exists:
    try:
        makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import sb
    sb.init_app(app)
    
    # from . import gmaps
    # gmaps.init_app(app)
    
    # from . import restaurant
    # app.register_blueprint(restaurant.bp)
    # app.add_url_rule('/', endpoint='index')
    
    return app
    
    