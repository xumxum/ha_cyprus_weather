#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re

from pprint import pprint
from bs4 import BeautifulSoup

BASE_URL   = 'https://www.cyprus-weather.org'

cityLink = {
    'Limassol'   : 'https://www.cyprus-weather.org/limassol-weather-forecast/', 
    'Nicosia'     : 'https://www.cyprus-weather.org/nicosia-weather-forecast/', 
    'Larnaca'     : 'https://www.cyprus-weather.org/larnaca-weather-forecast/', 
    'Paphos'       : 'https://www.cyprus-weather.org/paphos-weather-forecast/', 
    'Ayia napa'   : 'https://www.cyprus-weather.org/ayia-napa-weather-forecast/'
}

"""
Home assistant knows only about these states so it can map it to the icon
Otherwise won't display icon just the test 
Not sure where should be but better to return string then number for condition

clear-night
cloudy
fog
hail
lightning
lightning-rainy
partlycloudy
pouring
rainy
snowy
snowy-rainy
sunny
windy
windy-variant
exceptional
"""
conditions = {
    5:"windy",  #not clear if this is it
    32:"windy",  #not clear if this is it
    25:"hail", 
    26:"hail", 
    29:"snowy-rainy", 
    33:"clear-night", 
    34:"clear-night"
}

for key in [1, 2, 30, 31,]:
    conditions[key] = "sunny"
for key in [7, 8, 11, 37,]:
    conditions[key] = "cloudy"    
for key in [3, 4, 6,  35,  36,  38]:
    conditions[key] = "partlycloudy"    
for key in [12, 13, 14,  18,  39,  40]:
    conditions[key] = "rainy"
for key in [15, 16,  17, 41 ,  42]:
    conditions[key] = "lightning"    
for key in [19,  20,  21,  22,  23,  24,  43,  44]:
    conditions[key] = "snowy"    
    
def getData(city):
    page = requests.get( cityLink[city] )
    content = page.content

#    with open('./lim.html', 'r') as content_file:
#        content = content_file.read()        

    weatherData = {}

    re_condition_nr = re.compile('(\d+)\.svg')
    re_forecast_description = re.compile('<div class="description">(.+?)<')
    re_forecast_chanceofrain = re.compile('Chance of Rain: (\d+)%')
    re_forecast_wind = re.compile('(\d+) km\/h')
    re_forecast_temphigh = re.compile('<div class="temp temp-high">(\d+)')
    re_forecast_templow = re.compile('<div class="temp temp-low">(\d+)')
    #Sunrise: 06:34
    re_sunrise = re.compile('Sunrise:\s+(\d\d:\d\d)')
    re_sunset = re.compile('Sunset:\s+(\d\d:\d\d)')

    soup = BeautifulSoup(content, 'html.parser')        
    cwMain = soup.find(id="cwMain")

    currentIcon_s = str(cwMain.find_all("div",class_="currentIcon")[0])
    weatherData["Current.Description"]=(re.compile('alt="(.+?)"').findall(currentIcon_s)[0]).lower()
    condition_nr = re_condition_nr.findall(currentIcon_s)[0]
    weatherData["Current.Condition"]=conditions[ int (condition_nr) ]
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
        hourly_forecast_temperature = re.compile('/>\r?\n\s+(\d+).+\r?\n').findall(str(forecast_entry_s))[0]
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

    
    prefix=""
    for i in range(2):
        forecast_s = str(today_forecast_periods[i])
        prefix = "To" + (prefix_v[i]).lower()
                
        weatherData["Forecast." + prefix +".Description"] = re_forecast_description.findall(forecast_s)[0]
        weatherData["Forecast." + prefix +".ChanceOfRain"] = re_forecast_chanceofrain.findall(forecast_s)[0]
        weatherData["Forecast." + prefix +".Wind"] = re_forecast_wind.findall(forecast_s)[0]

        if i == 0:
            weatherData["Forecast." + prefix + ".TempHigh"] = re_forecast_temphigh.findall( forecast_s )[0]            
            weatherData["Forecast." + prefix + ".Sunrise"] = re_sunrise.findall( forecast_s )[0]            
        else:
            weatherData["Forecast." + prefix + ".TempLow"] = re_forecast_templow.findall( forecast_s )[0]
            weatherData["Forecast." + prefix + ".Sunset"] = re_sunset.findall( forecast_s )[0]            
    #pprint(weatherData)
    
    #dayly_forecast = cwMain.find_all("div",class_="forecast")[0]
    #re.compile("itl")
    dayly_forecast = cwMain.find_all("div",class_="forecast" )[1] #first is today forecast, ignore, was already processed 
    
    #pprint(str(dayly_forecast))
    
    day_container = dayly_forecast.find_all("div",class_="day-container")

    forecast_dayly={}
    day_counter = 0
    for day_container_entity in day_container:
        #day-date
        #pprint(day_container_entity)
        day_forecast_dict = {}
        
        day_date_s = str( day_container_entity.find_all("div",class_="day-date")[0] )
        #pprint(day_date_s)
        d = re.compile('<span>(.+?)\.\s*(\d+)(.+?)<').search(day_date_s)
        f_date = d.group(1) + " " + d.group(2) 
        day_forecast_dict["Date"] = f_date
        #pprint(f_date)
        
        day_forecast = day_container_entity.find_all("div",class_="day-forecast")[0] 
        forecast_periods = day_forecast.find_all("div",class_="period") 
        
        for i in range(2):
            forecast_s = str(forecast_periods[i])
            prefix = prefix_v[i] +"."

            description = re_forecast_description.findall(forecast_s)[0]
            chanceOfRain = re_forecast_chanceofrain.findall(forecast_s)[0]
            wind = re_forecast_wind.findall(forecast_s)[0]

            day_forecast_dict[prefix+"Description"] = description
            day_forecast_dict[prefix+"ChanceOfRain"] = chanceOfRain
            day_forecast_dict[prefix+"Wind"] = wind
            day_forecast_dict[prefix+"Condition"] = conditions[ int(re_condition_nr.findall( forecast_s )[0]) ]
            
            if i == 0:
                day_forecast_dict[prefix+"TempHigh"] = re_forecast_temphigh.findall( forecast_s )[0]
                #condition we take from day 
                #day_forecast_dict[prefix+"Condition"] = conditions[ int(re_condition_nr.findall( forecast_s )[0]) ]
            else:
                day_forecast_dict[prefix+"TempLow"] = re_forecast_templow.findall( forecast_s )[0]
       
        forecast_dayly[f_date] = day_forecast_dict
        day_counter = day_counter+1

    weatherData["Forecast"] = forecast_dayly
    
    #Extra summary and report strings to be sent to user and for speach i
    report = weatherData["Current.Condition"] + ", temperature is " + weatherData["Current.Temperature"]  + " degrees with maximum today " + weatherData["Forecast.Today.TempHigh"] + " degrees"
    
    windspeed = int(weatherData["Current.Wind"] )
    if windspeed > 50:
        windReport = ", very windy"
    else:
        if windspeed > 30:
            windReport = ", a bit windy"
    report = report + windReport
    
    rainChanceDay = int( weatherData["Forecast.Today.ChanceOfRain"] )
    rainChanceNight = int( weatherData["Forecast.Tonight.ChanceOfRain"] )

    rainProbdict = {}
    for k in range(0, 26):
        rainProbdict[k] = 'low chance of rain'
    for k in range(26, 51):
        rainProbdict[k] = 'moderate chance of rain'
    for k in range(51,  76):
        rainProbdict[k] = 'high chance of rain'
    for k in range(76,  101):
        rainProbdict[k] = 'very high chance of rain'

    rainReport = ''
    if rainChanceDay >= 50:
        rainReport = rainReport +", " + rainProbdict[rainChanceDay] + " during the day"
    if rainChanceNight >= 50:            
        rainReport = rainReport +" and " + rainProbdict[rainChanceNight] + " during the night"
    
    report = report + rainReport
    
    weatherData["Report"] = report
    
    return weatherData

_weatherData = getData('limassol')
pprint(_weatherData)


