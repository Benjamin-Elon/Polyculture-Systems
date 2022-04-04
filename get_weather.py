from datetime import datetime
from time import strftime

import seaborn
import matplotlib.pyplot as plt
from meteostat import Daily, Point
import requests
import json
from geopy.geocoders import Nominatim


def city_name_to_coords():
    geolocator = Nominatim(user_agent="polyculture_systems")
    location = geolocator.geocode("tzfat")
    print((location.latitude, location.longitude))
    print(location.raw)
    return location.latitude, location.longitude


def get_weather_data(lat, long):
    lat, long = city_name_to_coords()

    api_key = "254cd5f34fe9c65f99d62fee09b4c3d8"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    for x in data:
        print(x)
    print(data["current"])
    for x in data["current"]:
        print(x)


def get_historical_weather():
    lat, long = city_name_to_coords()
    day = datetime.now()
    todays_date = datetime.strftime(day, '%Y-%m-%d')
    todays_date = todays_date.split('-')

    # get last 2 years weather history
    start = datetime(int(todays_date[0])-10, 1, 1)
    end = datetime(int(todays_date[0]), int(todays_date[1]), int(todays_date[2]))
    weather_station_id = Point(lat, long)
    historical_weather = Daily(weather_station_id, start, end)
    # weather is a pandas dataframe
    historical_weather = historical_weather.fetch()

    for row in historical_weather.iterrows():
        for date in row:

            date = date.strftime('%Y-%m-%d')
            print(date)
            row['date'] = date
            print(historical_weather[row]['date'])
    for x in historical_weather['date']:
        print(x)

    # Plot line chart including average, minimum and maximum temperature
    # seaborn.histplot(x='prcp', data=historical_weather)
    plt.plot(x='prcp', y='date', data=historical_weather)
    # print(type(historical_weather))
    plt.show()

    df = historical_weather



get_historical_weather()
