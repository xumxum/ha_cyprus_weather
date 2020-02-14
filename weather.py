"""AEMET: Custom Weather Component for AEMET (Agencia Estatal de Metereologia)"""

import logging
from datetime import datetime
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.weather import PLATFORM_SCHEMA
from homeassistant.components.weather import WeatherEntity
from homeassistant.const import (
    CONF_NAME,
)
from homeassistant.const import PRECISION_TENTHS
from homeassistant.util import Throttle

#from .aemet import AemetData
#from .const import *

from .cyprus_weather_org import *

# Units
TEMP_CELSIUS = "°C"
TEMP_FAHRENHEIT = "°F"
DEFAULT_NAME = "cyweather"

CONF_SET_CITY = "city"
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_SET_CITY): cv.string,        
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the weather entities."""
    _LOGGER.debug("Setting up plataform %s", "cyprus_weather")

    name = config.get(CONF_NAME)
    city = config.get("city")

    add_entities([CyprusWeather(name, city)], True)
    _LOGGER.debug(
        "Entity created for city (%s)", city
    )


class CyprusWeather(WeatherEntity):
    """Representation of a weather entity."""

    def __init__(self, name, city):
        """Initialize Cyprus weather."""
        _LOGGER.debug("Creating instance of CyprusWeather, using parameters")
        _LOGGER.debug("name\t%s", name)
        _LOGGER.debug("city\t%s", city)

        self._name = name
        self._city = city

        #get initial weather data
        self.update()


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def temperature(self):
        """Return the temperature."""
        try:
            value = int(self._weatherData["Current.Temperature"])
            return value
        except:
            return None

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

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
    def pressure(self):
        """Return the pressure."""
        try:
            value = int(self._weatherData["Current.Pressure"])
            return value
        except:
            return None

    @property
    def wind_speed(self):
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
    def visibility(self):
        """Return the visibility."""
        try:
            value = int(self._weatherData["Current.Visibility"])
            return value
        except:
            return None

    """
    Home assistant knows only about these states so it can map it to the icon
    Otherwise won't display icon just the test 

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

    """Called every MIN_TIME_BETWEEN_UPDATES , updates the data values"""
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data"""
        _LOGGER.debug("Get the latest data from cyprus-weather.org for %s ", self._name)
        
        self._weatherData = getData(LIM)

	
