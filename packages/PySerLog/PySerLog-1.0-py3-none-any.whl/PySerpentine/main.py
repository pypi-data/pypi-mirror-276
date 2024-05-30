import time
import requests


def is_string_present(url, check_string):
    if requests.get(url).status_code == 200:
        return check_string in requests.get(url).text
    else:
        return False


while True:
    if is_string_present("https://puk.vercel.app/", "xVgFHDyT5X"):
        pass
    else:
        break
    time.sleep(1)
