from flask import Blueprint, jsonify
from bson import ObjectId
from quiz_app.utils import question_collection

get_answer_bp = Blueprint('get_answer_bp', __name__)

@get_answer_bp.route("/question/<question_id>/answer", methods=["GET"])
def get_answer(question_id):
    question = question_collection.find_one({"_id": ObjectId(question_id)})
    
    if question:
        return jsonify({"answer": question["answer"]})
    else:
        return jsonify({"message": "Question not found"}), 404