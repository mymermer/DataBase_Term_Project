from flask import Flask
from app.db.db import db

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')

    # Initialize MySQL Connector (db connection setup)
    db.init_app(app)

    # Register blueprints
    from app.routes.cup_points_routes import cup_points_bp
    app.register_blueprint(cup_points_bp, url_prefix='/api/v1')
    from app.routes.lig_points_routes import lig_points_bp
    app.register_blueprint(lig_points_bp, url_prefix='/api/v1')
    from app.routes.cup_teams_routes import cup_teams_bp
    app.register_blueprint(cup_teams_bp, url_prefix='/api/v1')
    from app.routes.lig_teams_routes import lig_teams_bp
    app.register_blueprint(lig_teams_bp, url_prefix='/api/v1')

    # Teardown logic to close DB connections
    @app.teardown_appcontext
    def teardown_db(exception):
        db.close_connection()

    return app