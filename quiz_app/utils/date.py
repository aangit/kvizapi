from datetime import datetime, timedelta

def is_timestamp_older_than_30_minutes(iso_timestamp):
    try:
        # Parse the ISO timestamp into a datetime object
        timestamp_datetime = datetime.fromisoformat(iso_timestamp)

        # Get the current time
        current_time = datetime.utcnow()

        # Calculate the time difference
        time_difference = current_time - timestamp_datetime

        # Check if the time difference is greater than or equal to 30 minutes
        if time_difference >= timedelta(minutes=30):
            return True
        else:
            return False
    except ValueError:
        # Handle invalid timestamp format
        return False
