from pyvalidator import is_mongo_id
from bson import ObjectId
from quiz_app.utils import user_collection
from datetime import datetime

class UserRepo:

    def find_by_id(id):
        if not is_mongo_id(id):
            return None

        return user_collection.find_one({ "_id": ObjectId(id) })

    def upsert_user(user_info):
        existing_user = user_collection.find_one({ "email": user_info["email"] })

        if existing_user is not None:
            user_info['updated_at'] = datetime.utcnow()
            user_collection.replace_one({ "_id": existing_user['_id'] }, user_info)
        else:
            user_info['created_at'] = datetime.utcnow()
            user_info['updated_at'] = datetime.utcnow()
            user_collection.insert_one(user_info)
