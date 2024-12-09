from flask import Flask
from app.db.db import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    # Load configuration
    app.config.from_object('app.config.Config')

    # Initialize MySQL Connector (db connection setup)
    db.init_app(app)

    # Register blueprints for points and teams tables
    from app.routes.cup_points_routes import cup_points_bp
    app.register_blueprint(cup_points_bp, url_prefix='/api/v1')
    from app.routes.lig_points_routes import lig_points_bp
    app.register_blueprint(lig_points_bp, url_prefix='/api/v1')
    from app.routes.cup_teams_routes import cup_teams_bp
    app.register_blueprint(cup_teams_bp, url_prefix='/api/v1')
    from app.routes.lig_teams_routes import lig_teams_bp
    app.register_blueprint(lig_teams_bp, url_prefix='/api/v1')

    # # Register blueprints for comparison and header tables
    # from app.routes.cup_comparison_routes import cup_comparison_bp
    # app.register_blueprint(cup_comparison_bp, url_prefix='/api/v1')
    # from app.routes.lig_comparison_routes import lig_comparison_bp
    # app.register_blueprint(lig_comparison_bp, url_prefix='/api/v1')
    # from app.routes.cup_header_routes import cup_header_bp
    # app.register_blueprint(cup_header_bp, url_prefix='/api/v1')
    # from app.routes.lig_header_routes import lig_header_bp
    # app.register_blueprint(lig_header_bp, url_prefix='/api/v1')
    

    # Teardown logic to close DB connections
    @app.teardown_appcontext
    def teardown_db(exception):
        db.close_connection()

    return app