from flask import Blueprint, jsonify, request
from quiz_app.utils import question_collection

add_question_bp = Blueprint('add_question_bp', __name__)

@add_question_bp.route('/question', methods=['POST'])
def add_question():
    data = request.json

    if isinstance(data, list):
        inserted_ids = []

        for entry in data:
            question_text = entry.get("question")
            
            if not question_text or question_collection.find_one({"question": question_text}):
                continue
            
            inserted = question_collection.insert_one(entry)
            inserted_ids.append(str(inserted.inserted_id))
        
        return jsonify({"message": "Questions added successfully", "inserted_ids": inserted_ids})
    
    elif isinstance(data, dict):
        question_text = data.get("question")
        
        if not question_text or question_collection.find_one({"question": question_text}):
            return jsonify({"message": "Question already exists or missing data"}), 400
        
        inserted_id = question_collection.insert_one(data).inserted_id
        return jsonify({"message": "Question added successfully", "inserted_id": str(inserted_id)})
    
    return jsonify({"message": "Invalid input data"}), 400