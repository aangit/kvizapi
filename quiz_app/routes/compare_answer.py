from flask import Blueprint, jsonify, request
from datetime import datetime
from quiz_app.repo import SessionRepo, QuestionRepo
from quiz_app.utils.date import is_timestamp_older_than_1_minute
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
    
    if 'latest_question' in session:
        latest_question = session['latest_question']

        if latest_question is not None and is_timestamp_older_than_1_minute(latest_question['created_at']):
            return "", 410

    question = QuestionRepo.find_by_id(question_id)

    if question is None:
        return jsonify({ "error": "question not found" }), 404

    answered_questions = session['answered_questions'] if 'answered_questions' in session else []

    if contains_object_with(answered_questions, 'question_id', question_id):
        return "", 410

    is_correct = question["answer"] == answer

    answered_questions.append({
        'question_id': question_id,
        'at': datetime.utcnow().isoformat(),
        'is_correct': is_correct
    })

    SessionRepo.update_answered_questions_by_id(session_id, answered_questions)

    score = SessionRepo.count_score(answered_questions)

    return jsonify({ "is_correct": is_correct, "score": score })
