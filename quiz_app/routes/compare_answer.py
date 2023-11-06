from flask import Blueprint, jsonify, request
from datetime import datetime
from quiz_app.repo import SessionRepo, QuestionRepo
from quiz_app.utils.date import is_timestamp_older_than_30_minutes
from quiz_app.utils.list import contains_object_with

compare_answer_bp = Blueprint('compare_answer_bp', __name__)

@compare_answer_bp.route("/question/<question_id>/answer", methods=["POST"])
def compare_answer(question_id):
    json_data = request.get_json()

    answer = json_data['answer']

    if answer is None or answer is '':
        return jsonify({ "error": "answer not provided" }), 400

    session_id = request.headers.get('X-Session-Id')

    session = SessionRepo.find_active_by_id(session_id)

    if session is None:
        return jsonify({ "error": "session not valid" }), 400

    question = QuestionRepo.find_by_id(question_id)

    if question is None:
        return jsonify({ "error": "question not found" }), 404

    answered_questions = session['answered_questions'] if 'answered_questions' in session else []

    if contains_object_with(answered_questions, 'question_id', question_id):
        return "", 410

    is_correct = question["answer"] == answer

    answered_questions.append({
        'question_id': question_id,
        'at': datetime.now().isoformat(),
        'is_correct': is_correct
    })

    SessionRepo.update_answered_questions_by_id(session_id, answered_questions)

    return jsonify({ "is_correct": is_correct, "score": SessionRepo.count_score(answered_questions) })
