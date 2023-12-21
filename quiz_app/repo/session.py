import uuid
from datetime import datetime
from quiz_app.utils import session_collection
from quiz_app.utils.date import has_expired, is_timestamp_older_than_30_minutes, increment_iso_timestamp

class SessionRepo:

    @staticmethod
    def create_session(user_id, minutes = 5):
        if minutes is None:
            minutes = 5

        session_id = str(uuid.uuid4())

        now = datetime.utcnow().isoformat()

        payload = {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': now,
            'expires_at': increment_iso_timestamp(now, minutes),
            'finished': False
        }
        session_collection.insert_one(payload)

        return payload

    @staticmethod
    def find_by_id(id):
        return session_collection.find_one({ "session_id": id })
    
    def find_active_by_id(id):
        session = session_collection.find_one({ "session_id": id })

        if session is None:
            return None

        expires_at = session['expires_at']

        if expires_at is None:
            return None

        if has_expired(expires_at) or 'finished' in session and session['finished']:
            return None
        
        return session
    
    def find_active_by_user_id(id):
        session = session_collection.find_one({ "user_id": id }, sort=[('expires_at', -1)] )

        if session is None:
            return None

        expires_at = session['expires_at']

        if expires_at is None:
            return None

        if has_expired(expires_at) or 'finished' in session and session['finished']:
            return None
        
        return session
    
    @staticmethod
    def update_answered_questions_by_id(id, answered_questions):
        if answered_questions is None:
            return

        session_collection.update_one(
            {
                "session_id": id
            },
            {
                '$set': {
                    'answered_questions': answered_questions,
                    'latest_question': None
                }
            }
        )
    
    @staticmethod
    def set_latest_question(id, question_id):
        session_collection.update_one({ "session_id": id }, { '$set': { 'latest_question': {
            "question_id": question_id,
            "created_at": datetime.utcnow().isoformat()
        } } })

    @staticmethod
    def finish_session(id):
        session_collection.update_one({ "session_id": id }, { '$set': { 'finished': True } })

    @staticmethod
    def count_score(answered_questions):
        score = 0

        if answered_questions is None:
            return score

        for aq in answered_questions:
            if aq['is_correct']:
                score += 1
            else:
                score -= 1
        
        return score
