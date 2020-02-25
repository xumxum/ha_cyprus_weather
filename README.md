# ha-cyprus-weather
Home Assistant Cyprus weather

## Description
Get Cyprus data from cyprus weather org site

### Installation
1. clone repo into your custom_components directory
> git clone https://github.com/xumxum/ha-cyprus-weather.git


2. Configuration in configure.yaml:
> weather:
>   platform: ha-cyprus-weather
>   city: 'Limassol'

3. Restart Home Assistant of course

Entity name will be weather.city (ex weather.nicosia), you can override it by defining also name parameter along the city

Possible cities:
Nicosia
Limassol
Larnaca
Paphos
Ayia Napa


