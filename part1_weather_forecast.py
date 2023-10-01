"""


requests error resource: https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module


"""

import logging
import requests
import os

api = 'https://api.openweathermap.org/data/2.5/forecast?/'
API_key = os.environ.get('WEATHER_API')

def main():

    payload, units = get_payload()

    temp_data, error = get_current_weather(payload)

    if error:
         print('error present: ' + str(error))
    else:
        display_local_temp(temp_data, units)


def get_payload():
        city = input('Enter a city to search for the current temperature: ').capitalize()

        code = input('Enter the 2 letter country code for ' + city + ': ')

        units = input('Choose "metric" for celsius or "imperial" for fahrenheit temperature: ').lower()

        while units not in ['metric', 'imperial']:
             units = input('Choose "metric" or "imperial" for temperature: ').lower()

        location = city + ',' + code

        payload = {'q': location, 'units': units, 'appid': API_key, 'timeout': 30}

        return payload, units

def get_current_weather(payload):
        try:
            logging.info(f'{payload} sent to {api}')
            response = requests.get(api, params=payload)
            response.raise_for_status()
            logging.debug(f'Call: {api} Payload: {payload} Status: {response.status_code}. Response received from API: {response}')
            data = response.json()
            return data, None
        except requests.HTTPError as HTerror:
            logging.exception(f'HTTP Error requesting weather: {HTerror}')
            return None, str(HTerror)
        except requests.exceptions.Timeout:
            error = 'Timeout Error requesting weather'
            logging.exception(error)
            return None, error
        except requests.exceptions.RequestException:
            error = 'Catastrophic error occurred'
            logging.exception(error)
            return None, error

        
def display_local_temp(data, units):

    forecast_day = 1

    if units == 'metric':
         units = 'c'
    else:
        units = 'f'

    city = data['city']['name']
    country = data['city']['country']

    print(f'\n--------------------------------------------')
    print(f'Displaying 5 day forecast: {city}, {country} \n')


    """
    TODO: Choosing Time - Part 2

    I chose to show the local time in Minneapolis, I added some light clarity by including the city name in the timestamp
    information.

    for example, when I went to DC and I looked at the weather for outdoor events during our trip. I didn't want to know that
    it would rain at 1 pm in minnesota and 2 pm in DC, or vice-versa for the trip home. I would need to know the local time for 
    the weather to be accurate 

    "We can go to the outdoor show, the rain starts an hour after it ends!- oooopppps!" 

    that leads to the real answer - the time you show depends entirely on the application purpose of the time.

    most instances may require documenting the UTC time in the cache and database, but converting that format to a 
    local time for the user with a method like this:
    
    https://docs.python.org/3/library/locale.html
    
    locale_info = locale.getlocale()
    get_language_code = locale_info['language_code']

    Note: I also added a forecast interval to give the program more clarity
    Future Update: Extract the date, and host the detail separate from time, thus giving the data more readability
    """


    for day in data['list']:
        print('Displaying '+ city + ' Forecast interval (3-hr): ' + str(forecast_day))
        print(city + ' Timestamp: ' + day['dt_txt'])
        print('Temperature: ' + str(day['main']['temp']) + units)
        print('Weather: ' + day['weather'][0]['description'])
        print('Wind Speed: ' + str(day['wind']['speed']) + '\n')
        forecast_day = forecast_day + 1

    print('Thank you for viewing da weather! \n')

if __name__ == '__main__':
    main()