from quiz_app.utils import session_collection
from quiz_app.utils.date import is_timestamp_older_than_30_minutes

class SessionRepo:

    @staticmethod
    def find_by_id(id):
        return session_collection.find_one({ "session_id": id })
    
    def find_active_by_id(id):
        session = session_collection.find_one({ "session_id": id })

        if session is None:
            return None

        created_at = session['created_at']

        if created_at is None:
            return None

        if is_timestamp_older_than_30_minutes(created_at):
            return None
        
        return session
    
    @staticmethod
    def update_answered_questions_by_id(id, answered_questions):
        if answered_questions is None:
            return

        session_collection.update_one({ "session_id": id }, { '$set': { 'answered_questions': answered_questions } })

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