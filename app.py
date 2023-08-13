from sre_constants import RANGE_UNI_IGNORE
from flask import Flask, jsonify, request
from pymongo import MongoClient
import random
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

mongo_db_uri = os.environ.get("MONGO_DB_URI")

if mongo_db_uri is None:
    raise ValueError ("mongo_db_uri is not available")

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(mongo_db_uri)
db = client['quiz']
question_collection = db['questions']

@app.route('/question', methods=['GET'])
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

    return jsonify(response)

@app.route('/question', methods=['POST'])
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

@app.route("/question/<question_id>/answer", methods=["GET"])
def get_answer(question_id):
    question = question_collection.find_one({"_id": ObjectId(question_id)})
    
    if question:
        return jsonify({"answer": question["answer"]})
    else:
        return jsonify({"message": "Question not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
