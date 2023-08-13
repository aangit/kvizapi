# from sre_constants import RANGE_UNI_IGNORE
from dotenv import load_dotenv
from flask import Flask
from quiz_app.routes import get_answer_bp
from quiz_app.routes import add_question_bp
from quiz_app.routes import get_question_bp
import os

app = Flask(__name__)

app.register_blueprint(get_answer_bp)
app.register_blueprint(add_question_bp)
app.register_blueprint(get_question_bp)

load_dotenv()

port = os.environ.get("PORTA")

if port is None:
    port = 5000

if __name__ == '__main__':
    app.run(debug=True,port=port)
