from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from controllers.inventory_controller import inventory_bp

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'sqlite:///inventory.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(inventory_bp, url_prefix='/products')
    
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)