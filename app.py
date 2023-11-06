import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from quiz_app.routes import get_answer_bp
from quiz_app.routes import add_question_bp
from quiz_app.routes import get_question_bp
from quiz_app.routes import start_session_bp

app = Flask(__name__)

allowed_origins = ["http://localhost:3000"]

CORS(app, origins=allowed_origins)

app.register_blueprint(get_answer_bp)
app.register_blueprint(add_question_bp)
app.register_blueprint(get_question_bp)
app.register_blueprint(start_session_bp)

load_dotenv()

port = os.environ.get("PORT")
host = os.environ.get("HOST")

if port is None:
    port = 5000
if host is None:
    host = "127.0.0.1"


if __name__ == '__main__':
    app.run(debug=True,port=port, host=host)
