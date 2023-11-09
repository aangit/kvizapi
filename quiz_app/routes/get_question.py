from flask import Blueprint, request
from bson import ObjectId
import random
from quiz_app.repo import SessionRepo, QuestionRepo
from quiz_app.utils.date import is_timestamp_older_than_1_minute

get_question_bp = Blueprint('get_question_bp', __name__)

@get_question_bp.route('/question', methods=['GET'])
def get_question():
    session_id = request.headers.get('X-Session-Id')

    session = SessionRepo.find_active_by_id(session_id)

    if session is not None and 'latest_question' in session:
        latest_question = session['latest_question']

        if latest_question is not None and not is_timestamp_older_than_1_minute(latest_question['created_at']):
            
            question = QuestionRepo.find_by_id(session['latest_question']['question_id'])

            # Shuffle the answers
            answers = random.sample(question['wrongs'], 3) + [question['answer']]
            random.shuffle(answers)

            # Prepare the response JSON
            response = {
                'question': question['question'],
                'answers': answers,
                'id': str(question["_id"]),
                'session_id': session['session_id']
            }

            return response

    answered_questions = session['answered_questions'] if session is not None and 'answered_questions' in session else []

    answered_question_ids = [ObjectId(answered_question["question_id"]) for answered_question in answered_questions]
    
    question = QuestionRepo.find_one_not_in_list(answered_question_ids)

    # Shuffle the answers
    answers = random.sample(question['wrongs'], 3) + [question['answer']]
    random.shuffle(answers)

    # Prepare the response JSON
    response = {
        'question': question['question'],
        'answers': answers,
        'id': str(question["_id"]),
    }

    if session is not None:
        response['session_id'] = session['session_id']

    SessionRepo.set_latest_question(session_id, response['id'])

    return response
