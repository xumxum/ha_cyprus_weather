[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# ha_cyprus_weather
Home Assistant Cyprus weather integration

## Description
Get Cyprus weather data from cyprus weather org site and display it in Home Assistant as a weather integration including forecast data.

## Installation
Integration can be installed manually by manually copying the integration to the custom_integration folder, or alternatively installed with HACS

### A. Manual Installation
1. clone repo to a working directory
> git clone https://github.com/xumxum/ha_cyprus_weather.git

2. Copy(or link) `./custom_components/ha_cyprus_weather` to your  HA custom_components directory

3. Add to `configure.yaml`:
```yaml
weather:
     - platform: ha_cyprus_weather
       city: 'Limassol'
```
Entity name will be `weather.city` (ex `weather.nicosia`), you can override it by defining optionaly the `name` parameter along the `city`

Possible cities:
- Nicosia
- Limassol
- Larnaca
- Paphos
- Ayia Napa

4. Restart Home Assistant of course

### B. HACS Installation
Now this integration can alternatively be easily installed with hacs as well, this is the recommanded way. More information about hacs on 
https://hacs.xyz/docs/basic/getting_started

1. Add the repo as a custom repository in hacs  
   https://github.com/xumxum/ha_cyprus_weather

2. Download Cyprus Weather integration in hacs

3. Add the configuration part same way as in manual installation above( no GUI config )

4. Restart Home Assistant

## Notes


For all the information it returns check the state attributes in developer section.

The `report` attribute is a weather report for the day, with current temperature, wind and rain forecasting (if it is foreseen) that can be sent to the user or used in a text-to-speach automation(for ex in the morning)
