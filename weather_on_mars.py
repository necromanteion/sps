'''
This script demonstrates using the requests library to retrieve weather data, sent by the Curiosity rover,
from NASA's {MAAS} API.
'''

import argparse
import requests

LATEST = 'http://marsweather.ingenology.com/v1/latest/'
ARCHIVE = 'http://marsweather.ingenology.com/v1/archive/'


def weather_data(start=None, end=None):
    '''Gathers weather data from the {MAAS} API and returns an iterator.'''

    url = ARCHIVE if start or end else LATEST

    params = {
        'terrestrial_date_start': start,
        'terrestrial_date_end': end
    }

    r = requests.get(url, params=params)

    try:
        for result in r.json()['results']:
            yield result

    except KeyError:
        yield r.json()['report']


def pretty_weather(data, fahrenheit=False):
    '''Formats weather data into a pleasant-looking string for terminal output.'''

    lines = ('\n'
             'Today on Mars will be {atmo_opacity} with a high of {max_temp} °C.\n'
             'Better bundle up for an overnight low of {min_temp} °C.\n'
             'Expect {pressure_string} pressure through the coming weeks, it\'s currently {pressure} bar!\n'
             'This information was last updated on {terrestrial_date}.\n')

    if fahrenheit:
        lines = lines.replace('temp', 'temp_fahrenheit')
        lines = lines.replace('°C', '°F')

    # **data will unpack the weather data into a bunch of keyword arguments
    # so format(**{'max_temp': 30.2, 'min_temp': -46.8}) becomes format(max_temp=30.2, min_temp=-46.8)
    return lines.format(**data)


def parse_args():
    '''Function called from the main script to parse command-line arguments.'''

    parser = argparse.ArgumentParser(description='Retrieve Mars weather data from NASA\'s {MAAS} API.')

    parser.add_argument('-d', '--date', help='date to grab weather data from in "YYYY-MM-DD" format')
    parser.add_argument('-f', '--fahrenheit', action='store_true', help='print results in Fahrenheit')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    data = next(weather_data(end=args.date))

    print(pretty_weather(data, fahrenheit=args.fahrenheit))