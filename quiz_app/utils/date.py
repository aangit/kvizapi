from datetime import datetime, timedelta

def is_timestamp_older_than_30_minutes(iso_timestamp):
    return is_timestamp_older_than_x_minutes(iso_timestamp, 30)

def is_timestamp_older_than_1_minute(iso_timestamp):
    return is_timestamp_older_than_x_minutes(iso_timestamp, 1)

def is_timestamp_older_than_x_minutes(iso_timestamp, x):
    iso_datetime = datetime.fromisoformat(iso_timestamp)
    
    iso_datetime_milliseconds = int(iso_datetime.timestamp() * 1000)

    minutesInMilliseconds = x * 60 * 1000

    current_time = datetime.utcnow()

    current_time_milliseconds = int(current_time.timestamp() * 1000)

    return iso_datetime_milliseconds + minutesInMilliseconds < current_time_milliseconds

def increment_iso_timestamp(iso_timestamp, minutes):
    dt = datetime.fromisoformat(iso_timestamp)
    
    dt_incremented = dt + timedelta(minutes=minutes)
    
    incremented_iso_timestamp = dt_incremented.isoformat()
    
    return incremented_iso_timestamp

def has_expired(iso_timestamp):
    current_utc = datetime.utcnow()

    provided_timestamp = datetime.fromisoformat(iso_timestamp)
    
    return current_utc > provided_timestamp
