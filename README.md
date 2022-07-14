[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# ha_cyprus_weather
Home Assistant Cyprus weather component

## Description
Get Cyprus weather data from cyprus weather org site

## Manual Installation
1. clone repo to a working directory
> git clone https://github.com/xumxum/ha_cyprus_weather.git

2. Copy(or link) `./custom_components/ha_cyprus_weather` to your  HA custom_components directory

2. Add to `configure.yaml`:
```yaml
weather:
     - platform: ha_cyprus_weather
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
