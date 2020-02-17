#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re

from pprint import pprint
from bs4 import BeautifulSoup

BASE_URL   = 'https://www.cyprus-weather.org'
LIM        = 'https://www.cyprus-weather.org/limassol-weather-forecast/'


def getData(url):
    #page = requests.get(url)
    #content = page.content

    with open('/tmp/lim.html', 'r') as content_file:
        content = content_file.read()        

    weatherData = {}

    soup = BeautifulSoup(content, 'html.parser')        
    cwMain = soup.find(id="cwMain")

    currentIcon_s = str(cwMain.find_all("div",class_="currentIcon")[0])
    weatherData["Current.Condition"]=(re.compile('alt="(.+?)"').findall(currentIcon_s)[0]).lower()
    weatherData["Current.OutlookIcon"]=BASE_URL + re.compile('src="(.+?)"').findall(currentIcon_s)[0]

    currentTemp_s = str(cwMain.find_all("div",class_="currentTemp")[0])    
    weatherData["Current.Temperature"] = re.compile('<div class="large">(.+?)°</div>').findall(currentTemp_s)[0]
    weatherData["Current.FeelsLike"] = re.compile('<div>Feels like (.+?)°</div>').findall(currentTemp_s)[0]

    currentDetails_s = str(cwMain.find_all("div",class_="currentDetails")[0])
    weatherData["Current.Humidity"] = re.compile('<th>Humidity:</th>\s+<td>(.+?)%</td>').findall(currentDetails_s)[0]
    weatherData["Current.Pressure"] = re.compile('<th>Pressure:</th>\s+<td>(.+?)\s*hPa</td>').findall(currentDetails_s)[0]
    weatherData["Current.DewPoint"] = re.compile('<th>Dew Point:</th>\s+<td>(.+?)°</td>').findall(currentDetails_s)[0]
    weatherData["Current.Visibility"] = re.compile('<th.+?Visibility:</th>\s+<td>(.+?)\s*km</td>').findall(currentDetails_s)[0]

    w = re.compile('<th>Wind:</th>\s+<td title="(.+?) km/h">(\w+)').search(currentDetails_s)    
    weatherData["Current.Wind"] = w.group(1)
    weatherData["Current.WindDirection"] = w.group(2)

    weatherData["Current.UVIndex"] = re.compile('<th>UV Index:</th>\s+<td>(.+?)</td>').findall(currentDetails_s)[0]

    #weatherData["Current.Condition"]="windy"

    #pprint(weatherData)

    return weatherData

_weatherData = getData(LIM)
pprint(_weatherData)


