# from sre_constants import RANGE_UNI_IGNORE
from flask import Flask
from quiz_app.routes import get_answer_bp
from quiz_app.routes import add_question_bp
from quiz_app.routes import get_question_bp

app = Flask(__name__)

app.register_blueprint(get_answer_bp)
app.register_blueprint(add_question_bp)
app.register_blueprint(get_question_bp)

if __name__ == '__main__':
    app.run(debug=True)
