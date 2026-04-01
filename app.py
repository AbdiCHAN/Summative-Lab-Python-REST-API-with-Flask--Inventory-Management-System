from flask import Flask
from controllers.inventory_controller import inventory_bp

app = Flask(__name__)
app.register_blueprint(inventory_bp)

if __name__ == '__main__':
    app.run(debug=True)