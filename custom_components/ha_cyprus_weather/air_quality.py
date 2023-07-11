#!/work/venv/zee/bin/python


import requests
import re
import datetime

from pprint import pprint
from bs4 import BeautifulSoup
#from datetime import datetime

BASE_URL   = 'https://www.airquality.dli.mlsi.gov.cy/'

"""
Pollutant	Low (1)	Moderate (2)	High (3)	Very High (4)
PM₁₀	0 - 50	50 - 100	100 - 200	> 200
PM₂.₅	0 - 25	25 - 50	50 - 100	> 100
O₃	0 - 100	100 - 140	140 - 180	> 180
NO₂	0 - 100	100 - 150	150 - 200	> 200
SO₂	0 - 150	150 - 250	250 - 350	> 350
CO	0 - 7000	7000 - 15000	15000 - 20000	> 20000
C₆H₆	0 - 5	5 - 10 	10 - 15 	> 15

PM₁₀	Particulate Matter 10 μm [μg/m³]
PM₂.₅	Particulate Matter 2.5 μm [μg/m³]
O₃	Ozone [μg/m³]
NO	Nitrogen Oxide [μg/m³]
NO₂	Nitrogen Dioxide [μg/m³]
NOx	Nitrogen Oxides [μg/m³]
SO₂	Sulfur Dioxide [μg/m³]
CO	Carbon Monoxide [μg/m³]
C₆H₆	Benzene [μg/m³]
"""
parameters = {
    'PM₁₀': {
        'levels':[50,100,200],
        'description': 'Particulate Matter 10 μm [μg/m³]',
        'unit_of_measurement': 'μg/m³',
        },
    'PM₂.₅': {
        'levels': [25,50,100]
        },
    'O₃' : {
        'levels':[100,140,180]
        },
    'NO₂' : {
        'levels': [100,150,200]
        },
    'SO₂' : {
        'levels':[150,250,350]
        },
    'CO' : {
        'levels': [7000,15000,20000]
        },
    'C₆H₆' : {
        'levels':[5,10,15]
        }
}

def getData(city):
#    page = requests.get( BASE_URL )
#    content = page.content

    with open('./air_quality_full.html', 'r') as content_file:
        content = content_file.read()

    rez = {}


    re_polutant_label = re.compile('<span class="pollutant-label">(.+?):<')
    re_polutant_value = re.compile('<span class="pollutant-value">([+-]?[0-9]*[.]?[0-9]+)')
    #<span class="pollutant-label">PM₂.₅:</span>
    #Sunrise: 06:34


    soup = BeautifulSoup(content, 'html.parser')
    stations = soup.find_all("div", class_="col-xs-12")
    for station in stations:
        if city in str(station):
            #span class="pollutant-field 
            fields = station.find_all("span", class_="pollutant-field")
            for field in fields:
                field_name = re_polutant_label.findall( str(field) )
                if field_name:
                    field_name = field_name[0].encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                    field_value = re_polutant_value.findall( str(field) )
                    if len(field_value): 
                        field_value = field_value[0]
                        try:
                            field_value = float(field_value)
                        except ValueError:
                            continue
                    d={}
                    d['value'] = field_value
                    d['polution_level'] = 0
                    if field_name in parameters:
                        d['polution_level'] = 1
                        for pl in parameters[field_name]['levels']:
                            if field_value >= pl:
                                 d['polution_level'] = d['polution_level'] + 1

                    #print(f'"{field_name}" -> "{field_value}"')
                    
                    rez[field_name] = d
                    

    return rez

#Test function
def test_getData():
    _weatherData = getData('Limassol')
    pprint(_weatherData)

if __name__ == '__main__':
    test_getData()
