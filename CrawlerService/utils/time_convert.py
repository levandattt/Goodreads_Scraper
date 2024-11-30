from datetime import datetime

def bdy_to_ymd(date_str):
    date_object = datetime.strptime(date_str, "%B %d, %Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    return formatted_date



