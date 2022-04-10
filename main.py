import json
import requests
import os
import sys
import datetime
from utils import parse_time
from dotenv import load_dotenv
import asyncio
import aiohttp
from copy import deepcopy
import math


async def sending_callback(data: dict, url: str, interval: int):
    while True:
        await asyncio.sleep(interval)
        data_to_send = deepcopy(data)
        data['time_series'].clear()
        print('sending data')
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data_to_send) as response:
                print(await response.json())


def get_x(settings: dict):
    x_current = settings['x_start']
    x_next = settings['x_start'] + settings['x_step']
    if x_next > settings['x_to'] or x_next < settings['x_from']:
        settings['x_step'] = - settings['x_step']
    settings['x_start'] = settings['x_start'] + settings['x_step']
    return x_current


async def main():
    config_file = sys.argv[1]
    assert os.path.isfile(config_file), 'Config file is not provided'

    with open(config_file, 'rt') as file:
        config = json.load(file)

    name = config['name']
    url = os.getenv('SERVER_URL')
    
    save_interval = parse_time(config['save_every'])
    send_interval = parse_time(config['send_every'])

    fields = config['fields']

    data = {
        "device_name": name,
        "time_series": []
    }

    asyncio.create_task(sending_callback(data, url, send_interval))

    while True:
        timestamp = {
            'stats': {},
            'date': str(datetime.datetime.now())
        }
        for field_name, settings in fields.items():
            x = get_x(settings)
            y = round(eval(settings['y'], {}, {'x': x, 'math': math}), 5)
            timestamp['stats'][field_name] = y
        print(f'generated {timestamp=}')
        data['time_series'].append(timestamp)

        await asyncio.sleep(save_interval)



if __name__ == '__main__':
    load_dotenv('.env')
    asyncio.run(main())