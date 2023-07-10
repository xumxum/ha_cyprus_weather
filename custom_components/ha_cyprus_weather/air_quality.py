#!/work/venv/zee/bin/python


import requests
import re
import datetime

from pprint import pprint
from bs4 import BeautifulSoup
#from datetime import datetime

BASE_URL   = 'https://www.airquality.dli.mlsi.gov.cy/'




def getData(city):
#    page = requests.get( BASE_URL )
#    content = page.content

    with open('./air_quality_full.html', 'r') as content_file:
        content = content_file.read()

    weatherData = {}


    re_polutant_label = re.compile('<span class="pollutant-label">(.+?)<')
    re_polutant_value = re.compile('<span class="pollutant-value">(\d+)')
    #<span class="pollutant-label">PM₂.₅:</span>
    #Sunrise: 06:34
    re_sunrise = re.compile('Sunrise:\s+(\d\d:\d\d)')
    re_sunset = re.compile('Sunset:\s+(\d\d:\d\d)')

    soup = BeautifulSoup(content, 'html.parser')
    stations = soup.find_all("div", class_="col-xs-12")
    for station in stations:
        if city in str(station):
            #span class="pollutant-field 
            fields = station.find_all("span", class_="pollutant-field")
            for field in fields:
                field_name = re_polutant_label.findall( str(field) )
                if field_name:
                    print(field_name)

    return weatherData

#Test function
def test_getData():
    _weatherData = getData('Limassol')
    pprint(_weatherData)

if __name__ == '__main__':
    test_getData()
