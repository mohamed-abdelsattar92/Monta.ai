from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import jwt as jwtLib

from montaai.config import Config
from montaai.helpers.database import db
from montaai.views.auth import auth_blueprint
from montaai.views.conversation import conversation_blueprint
from montaai.views.home import home_blueprint

app = Flask(__name__)
JWTManager(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(auth_blueprint)
app.register_blueprint(conversation_blueprint)
app.register_blueprint(home_blueprint)


@app.errorhandler(jwtLib.ExpiredSignatureError)
@app.errorhandler(jwtLib.InvalidTokenError)
def handle_invalid_token(error):
    return jsonify({"error": "Invalid or expired token"}), 401


@app.errorhandler(404)
def handle_not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def handle_internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
