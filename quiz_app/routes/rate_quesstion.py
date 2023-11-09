from flask import Blueprint
from quiz_app.repo.question import QuestionRepo

rate_question_bp = Blueprint('rate_question_bp', __name__)

@rate_question_bp.route('/question/<question_id>/uprate', methods=['GET'])
def uprate_question(question_id):

    QuestionRepo.rate(question_id, True)

    return "", 200

@rate_question_bp.route('/question/<question_id>/downrate', methods=['GET'])
def downrate_question(question_id):

    QuestionRepo.rate(question_id, False)

    return "", 200
