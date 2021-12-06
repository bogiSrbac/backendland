from datetime import datetime

def timestamp():
    date = datetime.now()
    # timestamp = date.strftime('%d-%m-%Y (%H:%M)')
    return date

print(timestamp())