from pyvalidator import is_mongo_id
from bson import ObjectId
from quiz_app.utils import question_collection

class QuestionRepo:

    def find_by_id(id):
        if not is_mongo_id(id):
            return None

        return question_collection.find_one({ "_id": ObjectId(id) })
    
    def find_one_not_in_list(list):
        pipeline = [
            {
                '$match': {
                    '_id': {
                        '$nin': list
                    }
                }
            },
            {
                '$sample': {
                    'size': 1
                }
            }
        ]

        return question_collection.aggregate(pipeline).next()
