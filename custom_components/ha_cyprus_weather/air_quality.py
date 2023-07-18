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
        'unit_of_measurement': 'µg/m³',
        'device_class': 'pm10'
        },
    'PM₂.₅': {
        'levels': [25,50,100],
        'description': 'Particulate Matter 2.5 μm [μg/m³]',
        'unit_of_measurement': 'µg/m³',
        'device_class': 'pm25'
        },
     'O₃' : {
        'levels':[100,140,180],
        'description': 'Ozone [μg/m³]',
        'unit_of_measurement': 'µg/m³',
        'device_class': 'ozone'
        },
    'NO' : {
        'levels': [100,150,200],
        'description': 'Nitrogen Monoxide',
        'unit_of_measurement': 'µg/m³',
        'device_class': 'nitrogen_monoxide'
        },        
    'NO₂' : {
        'levels': [100,150,200],
        'description': 'Nitrogen Dioxide',
        'unit_of_measurement': 'µg/m³',
        'device_class': 'nitrogen_dioxide'        
        },
    'NOx' : {
        'levels': [100,150,200],
        'description': 'Nitrogen Oxides [μg/m³]',
        'unit_of_measurement': 'µg/m³',
        'device_class': ''                
        },        
    'SO₂' : {
        'levels':[150,250,350],
        'description': 'Sulfur Dioxide [μg/m³]',
        'unit_of_measurement': 'µg/m³',
        'device_class': 'sulphur_dioxide'
        },
     'CO' : {
        'levels': [7,15,20],
        'description': 'Carbon Monoxide [ppm]',
        'unit_of_measurement': 'ppm',
        'device_class': 'carbon_monoxide'
        },
    'C₆H₆' : {
        'levels':[5,10,15],
        'description': 'Benzene [μg/m³]',
        'unit_of_measurement': 'µg/m³',
        'device_class': ''
        }
}

pollution_levels_str = {
    0:'unknown', 1:'Low',2:'Moderate',3:'High',4:'Very High'
}

def get_air_quality_parameters():
    return parameters

def get_air_quality_data(city):
    (measurements, _) = get_air_quality_all(city)
    return measurements

def get_air_quality_stations():
    (_, stations) = get_air_quality_all()
    return stations


def get_air_quality_all(city=''):
    
    page = requests.get( BASE_URL )
    content = page.content

    # text_file = open("/tmp/air_quality.html", "w")
    # text_file.write(str(content))
    # text_file.close()

    # with open('./air_quality_full.html', 'r') as content_file:
    #     content = content_file.read()

    rez = {}
    rez_station_names = []
    """
    <div class="views-field views-field-field-pollutant-38"><div class="field-content">
    <span class="pollutant-green">
    <span class="pollutant-field pollutant-label">NO:</span>
    <span class="pollutant-field pollutant-value">1.6 μg/m³</span>
    </span>
    </div></div>


    <div class="views-field views-field-field-pollutant-10"><div class="field-content">
    <span class="pollutant-field pollutant-green">
    <span class="pollutant-label">CO:</span>
    <span class="pollutant-value">321.3 μg/m³</span>
    </span>
    </div></div>

    """

    re_polutant_label = re.compile('<span class=".*?pollutant-label">(.+?):<')
    re_polutant_value = re.compile('<span class=".*?pollutant-value">([+-]?[0-9]*[.]?[0-9]+)')
    
    #<h4 class="field-content stations-overview-title">Limassol - Traffic Station</h4>
    re_station_name = re.compile('<h4 class=".*?stations-overview-title">(.+?)<')
    #<span class="pollutant-label">PM₂.₅:</span>
    #Sunrise: 06:34


    soup = BeautifulSoup(content, 'html.parser')
    stations_sections = soup.find_all("div", class_="views-row")
    for station in stations_sections:
        if city and city in str(station):
            #span class="field-content 
            #print(str(station))
            #print("**************************************************")
            #print("**************************************************")
            fields = station.find_all("div", class_="views-field")
            for field in fields:
                #print(str(field))
                #print("===================================================")
                field_name = re_polutant_label.findall( str(field) )
                if field_name:
                    field_name = field_name[0].encode().decode('unicode-escape').encode('latin1').decode('utf-8')
                    field_value = re_polutant_value.findall( str(field) )

                    #print(f'field_valueB = {field_value}')
                    if len(field_value) == 1: 
                        field_value = field_value[0]
                        try:
                            field_value = float(field_value)
                            if field_name == 'CO': #convert to ppm by diving with 1000
                                field_value = field_value / 1000.0
                        except Exception as ex:
                            print("Exception: ", ex)
                            continue
                    else:
                        continue

                    #print(f'field_valueA = {field_value}')
                    d={}
                    d['value'] = field_value
                    polution_level = 0
                    if field_name in parameters:
                        if 'description' in parameters[field_name]:
                            d['description'] = parameters[field_name]['description']
                        if 'unit_of_measurement' in parameters[field_name]:
                            d['unit_of_measurement'] = parameters[field_name]['unit_of_measurement']

                        polution_level = 1
                        for pl in parameters[field_name]['levels']:
                            if field_value >= pl:
                                 polution_level = polution_level + 1
                    d['polution_level'] = pollution_levels_str[polution_level]

                    #print(f'"{field_name}" -> "{field_value}"')
                    
                    rez[field_name] = d
                    
    #<h4 class="field-content stations-overview-title">Limassol - Traffic Station</h4>
    stations = soup.find_all("h4", class_="stations-overview-title")
    for station in stations:
        finds = re_station_name.findall( str(station) )
        if finds:
            station_name = str(finds[0])
            #print(f"Station: {station_name}")
            rez_station_names.append(station_name)

    return (rez,rez_station_names)

#Test function
def test_getData():
    _stations = get_air_quality_stations()
    pprint(_stations)
    print("****************************************")
    _weatherData = get_air_quality_data('Limassol')
    pprint(_weatherData)

if __name__ == '__main__':
    test_getData()
