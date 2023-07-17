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

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

#from .cyprus_weather_org import *
from .const import DEFAULT_NAME, DOMAIN, CONF_CITY

from .coordinator import CyprusWeatherUpdateCoordinator

# Units

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)

 
_LOGGER = logging.getLogger(__name__)



async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Cyprus weather based on a config entry."""
    city = entry.data.get(CONF_CITY)
    name = entry.data.get(CONF_NAME, city)

    async_add_entities(
        [
            CyprusWeather(
                hass=hass,
                name=name,
                city=city,
                coordinator=hass.data[DOMAIN][entry.entry_id],
                entry_id=entry.entry_id,
            )
        ]
    )



class CyprusWeather(WeatherEntity):
    """Representation of a weather entity."""
    _attr_native_temperature_unit = TEMP_CELSIUS
    _attr_native_precipitation_unit = LENGTH_MILLIMETERS
    _attr_native_pressure_unit = PRESSURE_HPA
    _attr_native_wind_speed_unit = SPEED_METERS_PER_SECOND

    def __init__(self, hass, name, city, coordinator, entry_id):
        """Initialize Cyprus weather."""
        _LOGGER.debug("Creating instance of CyprusWeather, using parameters")
        _LOGGER.debug("name\t%s", name)
        _LOGGER.debug("city\t%s", city)

        self._hass = hass
        self._name = name
        self._city = city
        self._coordinator = coordinator

        self._attr_unique_id = f"{entry_id}-{DEFAULT_NAME} {city} "  

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_temperature(self):
        """Return the temperature."""
        try:
            value = int(self._coordinator.get_weather_value("Current.Temperature"))
            return value
        except:
            return None

    @property
    def humidity(self):
        """Return the humidity."""
        try:
            value = int(self._coordinator.get_weather_value("Current.Humidity"))
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
            value = self._coordinator.get_weather_value("Current.Condition")
            return value
        except:
            return None

    @property
    def native_pressure(self):
        """Return the pressure."""
        try:
            value = int(self._coordinator.get_weather_value("Current.Pressure"))
            return value
        except:
            return None

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        try:
            value = int(self._coordinator.get_weather_value("Current.Wind"))
            return value
        except:
            return None

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        try:
            value = self._coordinator.get_weather_value("Current.WindDirection")
            return value
        except:
            return None

    @property
    def native_visibility(self):
        """Return the visibility."""
        try:
            value = int(self._coordinator.get_weather_value("Current.Visibility"))
            return value
        except:
            return None
   
    @property
    def forecast(self):
        """Return the forecast array."""
        rez = []
        forecast_d = self._coordinator.get_weather_value("Forecast")
        if forecast_d:
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
        forecast_temp_high = self._coordinator.get_weather_value("Forecast.Today.TempHigh")
        if forecast_temp_high:
            data["forecast_temp_high"] = forecast_temp_high
        
        forecast_temp_low = self._coordinator.get_weather_value("Forecast.Tonight.TempLow")
        data["forecast_temp_low"] = forecast_temp_low

        #this a string report, can be used in tts speach in a morning automation for example
        report =  self._coordinator.get_weather_value("Report")
        if report:
            data["report"] = report
        
        return data
    

	
