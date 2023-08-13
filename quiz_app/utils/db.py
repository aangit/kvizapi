from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

mongo_db_uri = os.environ.get("MONGO_DB_URI")

if mongo_db_uri is None:
    raise ValueError ("mongo_db_uri is not available")

client = MongoClient(mongo_db_uri)
db = client['quiz']
question_collection = db['questions']

