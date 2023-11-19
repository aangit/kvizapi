import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from quiz_app.routes import (
    get_answer_bp,
    add_question_bp,
    get_question_bp,
    start_session_bp,
    compare_answer_bp,
    rate_question_bp,
    oauth_bp
)

app = Flask(__name__)

allowed_origins = ["http://localhost:3000"]

CORS(app, origins=allowed_origins)

app.register_blueprint(get_answer_bp)
app.register_blueprint(add_question_bp)
app.register_blueprint(get_question_bp)
app.register_blueprint(start_session_bp)
app.register_blueprint(compare_answer_bp)
app.register_blueprint(rate_question_bp)
app.register_blueprint(oauth_bp)

load_dotenv()

port = os.environ.get("PORT")
host = os.environ.get("HOST")

if port is None:
    port = 5001
if host is None:
    host = "127.0.0.1"


if __name__ == '__main__':
    app.run(debug=True,port=port, host=host)
