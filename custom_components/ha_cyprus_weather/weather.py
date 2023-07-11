"""Cyprus Weather Component"""

import logging
#from datetime import datetime
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.temperature import display_temp as show_temp

import voluptuous as vol
from homeassistant.components.weather import *

from homeassistant.const import (
    CONF_NAME,
    CONF_MODE,
    LENGTH_MILLIMETERS,
    PRESSURE_HPA,
    SPEED_METERS_PER_SECOND,
    TEMP_CELSIUS,
)
from homeassistant.const import PRECISION_TENTHS
from homeassistant.util import Throttle


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .cyprus_weather_org import *

# Units

CONF_CITY = "city"
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)

 
_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CITY): cv.string,         
        vol.Optional(CONF_NAME): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the weather entities."""
    _LOGGER.debug("Setting up plataform %s", "ha_cyprus_weather")

    name = config.get(CONF_NAME)
    city = config.get(CONF_CITY)
    
    if not name :
        name = city

    city = city.capitalize() #makeing sure lowercase   
    
    add_entities([CyprusWeather(hass,  name, city)], True)
    _LOGGER.debug(
        "Entity created for city (%s)", city
    )
    #add_entities([ExampleSensor()])


class CyprusWeather(WeatherEntity):
    """Representation of a weather entity."""
    _attr_native_temperature_unit = TEMP_CELSIUS
    _attr_native_precipitation_unit = LENGTH_MILLIMETERS
    _attr_native_pressure_unit = PRESSURE_HPA
    _attr_native_wind_speed_unit = SPEED_METERS_PER_SECOND

    def __init__(self, hass,  name, city):
        """Initialize Cyprus weather."""
        _LOGGER.debug("Creating instance of CyprusWeather, using parameters")
        _LOGGER.debug("name\t%s", name)
        _LOGGER.debug("city\t%s", city)

        self.hass = hass
        self._name = name
        self._city = city

        #get initial weather data
        self.update()


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_temperature(self):
        """Return the temperature."""
        try:
            value = int(self._weatherData["Current.Temperature"])
            return value
        except:
            return None

    @property
    def humidity(self):
        """Return the humidity."""
        try:
            value = int(self._weatherData["Current.Humidity"])
            return value
        except:
            return None

    @property
    def precision(self):
        return PRECISION_TENTHS

    @property
    def condition(self):
        """Return the weather condition."""
        try:
            value = self._weatherData["Current.Condition"]
            return value
        except:
            return None

    @property
    def native_pressure(self):
        """Return the pressure."""
        try:
            value = int(self._weatherData["Current.Pressure"])
            return value
        except:
            return None

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        try:
            value = int(self._weatherData["Current.Wind"])
            return value
        except:
            return None

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        try:
            value = self._weatherData["Current.WindDirection"]
            return value
        except:
            return None

    @property
    def native_visibility(self):
        """Return the visibility."""
        try:
            value = int(self._weatherData["Current.Visibility"])
            return value
        except:
            return None
   
    @property
    def forecast(self):
        """Return the forecast array."""
        rez = []
        forecast_d = self._weatherData["Forecast"]
        for k in forecast_d:
            forecast_entry = {
                ATTR_FORECAST_TIME: forecast_d[k]["Date"],
                ATTR_FORECAST_NATIVE_TEMP: int(forecast_d[k]["Day.TempHigh"]),
                ATTR_FORECAST_NATIVE_TEMP_LOW: int(forecast_d[k]["Night.TempLow"]), 
                ATTR_FORECAST_CONDITION: forecast_d[k]["Day.Condition"] # we show daytime forecast condition not night?!!
            }
            rez.append(forecast_entry)
        
        return rez
                

    @property
    def state_attributes(self):
        """Return the state attributes."""
        data = {}
        
        temperature = self.native_temperature
        if self.native_temperature is not None:
            data[ATTR_WEATHER_TEMPERATURE] = temperature

        humidity = self.humidity
        if humidity is not None:
            data[ATTR_WEATHER_HUMIDITY] = round(humidity)

        ozone = self.ozone
        if ozone is not None:
            data[ATTR_WEATHER_OZONE] = ozone

        pressure = self.native_pressure
        if pressure is not None:
            data[ATTR_WEATHER_PRESSURE] = pressure

        wind_bearing = self.wind_bearing
        if wind_bearing is not None:
            data[ATTR_WEATHER_WIND_BEARING] = wind_bearing

        wind_speed = self.native_wind_speed
        if wind_speed is not None:
            data[ATTR_WEATHER_WIND_SPEED] = wind_speed

        visibility = self.native_visibility
        if visibility is not None:
            data[ATTR_WEATHER_VISIBILITY] = visibility

        attribution = self.attribution
        if attribution is not None:
            data[ATTR_WEATHER_ATTRIBUTION] = attribution

        forecast = self.forecast
        if forecast is not None:
            data[ATTR_FORECAST] = forecast

        # #add our own custom stuff
        data["forecast_temp_high"] = self._weatherData["Forecast.Today.TempHigh"]
        data["forecast_temp_low"] = self._weatherData["Forecast.Tonight.TempLow"]

        #this a string report, can be used in tts speach in a morning automation for example
        data["report"] = self._weatherData["Report"]
        
        return data
    

    """Called every MIN_TIME_BETWEEN_UPDATES , updates the data values"""
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data"""
        _LOGGER.debug("Get the latest data from cyprus-weather.org for %s ", self._city)
        new_data = getData(self._city)
        #if we fail to scrape there will be no data showing..
        #lets try this aproach ...if scraping failed, just leave the old data..
        if new_data:
            self._weatherData = new_data

	
