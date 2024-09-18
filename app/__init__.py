from flask import Flask, jsonify
from app.config import Config  # 修正箇所

app = Flask(__name__)
app.config.from_object(Config)

from app.route import main_bp
app.register_blueprint(main_bp)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Invalid endpoint"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"message": "Method not allowed"}), 405
