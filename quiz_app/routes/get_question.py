from flask import Blueprint, jsonify
import random
from quiz_app.utils import question_collection

get_question_bp = Blueprint('get_question_bp', __name__)

@get_question_bp.route('/question', methods=['GET'])
def get_question():
    # Get a random question from the collection
    question = question_collection.aggregate([{ '$sample': { 'size': 1 } }]).next()

    # Shuffle the answers
    answers = random.sample(question['wrongs'], 3) + [question['answer']]
    random.shuffle(answers)

    # Prepare the response JSON
    response = {
        'question': question['question'],
        'answers': answers,
        'id': str(question["_id"])
    }

    return response