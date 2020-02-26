# ha-cyprus-weather
Home Assistant Cyprus weather component

## Description
Get Cyprus weather data from cyprus weather org site

## Installation
1. clone repo into your HA custom_components directory
> git clone https://github.com/xumxum/ha-cyprus-weather.git


2. Add to `configure.yaml`:
```yaml
weather:
     - platform: ha-cyprus-weather
       city: 'Limassol'
```

3. Restart Home Assistant of course

Entity name will be weather.city (ex weather.nicosia), you can override it by defining also name parameter along the city

Possible cities:
- Nicosia
- Limassol
- Larnaca
- Paphos
- Ayia Napa


## Notes
For all the information it returns check the state attributes in developer section. 

The `report` attribute is a weather report for the day, with current temperature, wind and rain forecasting (if it is foreseen) that can be sent to the user or used in a text-to-speach automation(for ex in the morning)