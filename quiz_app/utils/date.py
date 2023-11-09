from datetime import datetime

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
    
    print (iso_datetime_milliseconds, minutesInMilliseconds, current_time_milliseconds)

    return iso_datetime_milliseconds + minutesInMilliseconds < current_time_milliseconds
