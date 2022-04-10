import requests
import sys
import datetime
from random import randint
from dotenv import load_dotenv


def main():
    url = sys.argv[1]
    name = 'test_device-satgB21'
    start_date = datetime.datetime.now() - datetime.timedelta(days=randint(10, 100))
    base_data = {
        "temp": 52.62,
        "speed": 20,
        "storage": 0.1
    }

    requests.post(
        url,
        json={
            "device_name": name,
            "time_series": [{"stats": base_data, "date": str(start_date + datetime.timedelta(minutes=minute))} for minute in range(0, 60, 10)]
        }
    )

if __name__ == '__main__':
    load_dotenv('.env')
    main()