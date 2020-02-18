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
    
    #Hourly forecast data
    forecasts_v = cwMain.find_all("div",class_="hour")
    forecast_hourly={}
    for forecast_entry_s in forecasts_v:
        #pprint(forecast_entry_s)
        hourly_forecast_time = re.compile('>\s*(.+?)\s*<').findall(str(forecast_entry_s))[0]
        #pprint(hourly_forecast_time)
        hourly_forecast_temperature = re.compile('/>\r\n\s+(\d+).+\r\n').findall(str(forecast_entry_s))[0]
        #d = re.compile('>\s*(.+?)\s*<').findall(str(forecast_entry_s))[0]
        #pprint(hourly_forecast_temperature)
        #forecast_hourly.append()
        forecast_hourly[hourly_forecast_time] = hourly_forecast_temperature
    #pprint(forecast_hourly)
    
    weatherData["Forecast.Hourly"] = forecast_hourly
    
    #Today forecast
    #<div class="day-forecast">
    today_forecast = cwMain.find_all("div",class_="forecast thisDay")[0]
    #first is daytime, 2nd is nighttime
    today_forecast_periods = today_forecast.find_all("div",class_="period") 
    prefix_v=['Day', 'Night']
    for i in range(2):
        forecast_s = str(today_forecast_periods[i])
        prefix = prefix_v[i]
                
        weatherData["Forecast." + prefix +".Description"] = re.compile('<div class="description">(.+?)<').findall(forecast_s)[0]
        weatherData["Forecast." + prefix +".ChanceOfRain"] = re.compile('Chance of Rain: (\d+)%').findall(forecast_s)[0]
        weatherData["Forecast." + prefix +".Wind"] = re.compile('(\d+) km\/h').findall(forecast_s)[0]

    weatherData["Forecast." + prefix_v[0] + ".TempHigh"] = re.compile('<div class="temp temp-high">(\d+)').findall( str(today_forecast_periods[0]) )[0]
    weatherData["Forecast." + prefix_v[1] + ".TempLow"] = re.compile('<div class="temp temp-low">(\d+)').findall( str(today_forecast_periods[1]) )[0]
    #pprint(weatherData)
    
    #dayly_forecast = cwMain.find_all("div",class_="forecast")[0]
    #re.compile("itl")
    dayly_forecast = cwMain.find_all("div",class_="forecast" )[1] #first is today forecast, ignore, was already processed 
    
    #pprint(str(dayly_forecast))
    
    day_container = dayly_forecast.find_all("div",class_="day-container")

    forecast_dayly={}
    for day_container_entity in day_container:
        #day-date
        #pprint(day_container_entity)
        day_date_s = str( day_container_entity.find_all("div",class_="day-date")[0] )
        f_date = re.compile('<span>(.+?)<').findall(day_date_s)[0]
        
        pprint(f_date)


    return weatherData

_weatherData = getData(LIM)
pprint(_weatherData)


