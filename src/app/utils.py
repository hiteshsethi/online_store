import datetime


def get_current_timestamp():
    return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
