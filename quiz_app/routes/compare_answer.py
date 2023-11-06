from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from datetime import datetime
from pyvalidator import is_mongo_id
from quiz_app.utils import question_collection, session_collection
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

    session = session_collection.find_one({ "session_id": session_id })

    if session is None or is_timestamp_older_than_30_minutes(session['created_at']):
        return jsonify({ "error": "session not valid" }), 400
    
    is_valid_mongo_id = is_mongo_id(question_id)

    if not is_valid_mongo_id:
        return jsonify({ "error": "question not found" }), 404

    question = question_collection.find_one({ "_id": ObjectId(question_id) })

    if question is None:
        return jsonify({ "error": "question not found" }), 404

    correct_q = session['correct_answered_questions'] if 'correct_answered_questions' in session else []
    incorrect_q = session['incorrect_answered_questions'] if 'incorrect_answered_questions' in session else []

    if contains_object_with(correct_q, 'question_id', question_id) or contains_object_with(incorrect_q, 'question_id', question_id):
        return "", 410

    is_correct = question["answer"] == answer

    if is_correct:
        correct_q.append({
            'question_id': question_id,
            'at': datetime.now().isoformat()
        })
    else:
        incorrect_q.append({
            'question_id': question_id,
            'at': datetime.now().isoformat()
        })

    session['correct_answered_questions'] = correct_q
    session['incorrect_answered_questions'] = incorrect_q

    session_collection.update_one({ "session_id": session_id }, { '$set': session })

    return jsonify({ "is_correct": is_correct, "score": len(correct_q) - len(incorrect_q) })
