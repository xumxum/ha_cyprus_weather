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
)
from homeassistant.const import PRECISION_TENTHS
from homeassistant.util import Throttle

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

    add_entities([CyprusWeather(hass,  name, city)], True)
    _LOGGER.debug(
        "Entity created for city (%s)", city
    )


class CyprusWeather(WeatherEntity):
    """Representation of a weather entity."""

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
    
    @property
    def state_attributes(self):
        """Return the state attributes."""
        data = {}
        
        if self.temperature is not None:
            data[ATTR_WEATHER_TEMPERATURE] = show_temp(
                self.hass, self.temperature, self.temperature_unit, self.precision
            )

        humidity = self.humidity
        if humidity is not None:
            data[ATTR_WEATHER_HUMIDITY] = round(humidity)

        ozone = self.ozone
        if ozone is not None:
            data[ATTR_WEATHER_OZONE] = ozone

        pressure = self.pressure
        if pressure is not None:
            data[ATTR_WEATHER_PRESSURE] = pressure

        wind_bearing = self.wind_bearing
        if wind_bearing is not None:
            data[ATTR_WEATHER_WIND_BEARING] = wind_bearing

        wind_speed = self.wind_speed
        if wind_speed is not None:
            data[ATTR_WEATHER_WIND_SPEED] = wind_speed

        visibility = self.visibility
        if visibility is not None:
            data[ATTR_WEATHER_VISIBILITY] = visibility

        attribution = self.attribution
        if attribution is not None:
            data[ATTR_WEATHER_ATTRIBUTION] = attribution

        if self.forecast is not None:
            forecast = []
            for forecast_entry in self.forecast:
                forecast_entry = dict(forecast_entry)
                forecast_entry[ATTR_FORECAST_TEMP] = show_temp(
                    self.hass,
                    forecast_entry[ATTR_FORECAST_TEMP],
                    self.temperature_unit,
                    self.precision,
                )
                if ATTR_FORECAST_TEMP_LOW in forecast_entry:
                    forecast_entry[ATTR_FORECAST_TEMP_LOW] = show_temp(
                        self.hass,
                        forecast_entry[ATTR_FORECAST_TEMP_LOW],
                        self.temperature_unit,
                        self.precision,
                    )
                forecast.append(forecast_entry)

            data[ATTR_FORECAST] = forecast

        #add our own custom shit
        data["forecast_temp_low"]=5
        data["forecast_temp_high"]=45
        return data
    

    """Called every MIN_TIME_BETWEEN_UPDATES , updates the data values"""
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data"""
        _LOGGER.debug("Get the latest data from cyprus-weather.org for %s ", self._name)
        
        self._weatherData = getData(LIM)

	
