"""DataUpdateCoordinator for knmi."""
import logging
from typing import Any, Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL

from .cyprus_weather_org import get_weather_data
from .air_quality import get_air_quality_data



_LOGGER: logging.Logger = logging.getLogger(__package__)

WEATHER_KEY = 'weather'
AIR_QUALITY_KEY = 'air_quality'

class CyprusWeatherUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data"""

    config_entry: ConfigEntry

    def __init__( self, hass: HomeAssistant,  city ) -> None:
        """Initialize."""
        #self.api = client
        #self.device_info = device_info


        self._city = city
        self._hass = hass

        super().__init__(
            hass=hass, logger=_LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL
        )

    # async def _async_update_data(self) -> dict[str, Any]:
    #     """Update data """
    #     try:
    #         return await self.api.async_get_data()
    #     except Exception as exception:
    #         _LOGGER.error("Update failed! - %s", exception)
    #         raise UpdateFailed() from exception

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data """
        try:
            rez = {}
            #both data, same dictionary under different keys
            _LOGGER.debug("Get the latest data from cyprus-weather.org for %s ", self._city)
            newWeatherData = await self._hass.async_add_executor_job(get_weather_data,self._city)
            rez[WEATHER_KEY] = newWeatherData

            _LOGGER.debug("Get the latest data from www.airquality.dli.mlsi.gov.cy for %s ", self._city)
            newAirQualityData = await self._hass.async_add_executor_job(get_air_quality_data,self._city)
            rez[AIR_QUALITY_KEY] = newAirQualityData

            return rez
        except Exception as exception:
            _LOGGER.error("Update failed! - %s", exception)
            raise UpdateFailed() from exception

    def get_weather_value( self, key: str ) -> float | int | str | None:
        if self.data and WEATHER_KEY in self.data and key in self.data[WEATHER_KEY]:
            return self.data[WEATHER_KEY].get(key, None)

        _LOGGER.warning("Value %s is missing in API response", key)
        return None
    
    def get_air_quality_value( self, key: str ) -> float | int | str | None:
        if self.data and AIR_QUALITY_KEY in self.data and key in self.data[AIR_QUALITY_KEY]:
            return self.data[AIR_QUALITY_KEY].get(key, None)

        _LOGGER.warning("Value %s is missing in API response", key)
        return None    