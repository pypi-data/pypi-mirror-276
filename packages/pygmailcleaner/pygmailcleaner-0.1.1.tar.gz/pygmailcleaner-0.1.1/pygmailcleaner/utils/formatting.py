import time
import datetime

def get_unix_timestamp(date_char):
    dto = datetime.datetime.strptime(date_char, "%Y-%m-%d")
    return round(time.mktime(dto.timetuple()))


def return_logo():
    return r"""
    ____ ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ ____ 
    ||P |||Y |||G |||M |||A |||I |||L |||       |||C |||L |||E |||A |||N |||E |||R ||
    ||__|||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__|||__||
    |/__\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/__\| 
            
    """