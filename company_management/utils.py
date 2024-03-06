import pytz

def formatted_timestamp(timestamp):
    local_timezone = pytz.timezone('Asia/Kolkata')
    local_time = timestamp.astimezone(local_timezone)
    return local_time.strftime("%I:%M %p %A, %b %d, %Y")


