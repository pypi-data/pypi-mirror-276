from datetime import datetime, timedelta


def now_timestamp_plus_minutes(minutes: int) -> str:
    now = datetime.utcnow()
    future_time = now + timedelta(minutes=minutes)
    timestamp = future_time.strftime("%Y-%m-%dT%H:%M:%S") + ".{:03d}Z".format(
        int(future_time.microsecond / 1000)
    )

    return timestamp
