"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.const import CONF_NAME, PERCENTAGE, TEMP_CELSIUS, UnitOfSpeed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


from .const import DEFAULT_NAME, DOMAIN, CONF_CITY

from .coordinator import CyprusWeatherUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


weather_sensors: list[SensorEntityDescription] = [
    SensorEntityDescription(
        key="Current.Temperature",
        name="Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Current.Humidity",
        name="Humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY, #?
        state_class=SensorStateClass.MEASUREMENT,
    )
]

air_quality_sensors: list[SensorEntityDescription] = [
    SensorEntityDescription(
        key="PM₁₀",
        name="PM₁₀",
        native_unit_of_measurement='µg/m³',
        device_class=SensorDeviceClass.PM10, #?
        state_class=SensorStateClass.MEASUREMENT,
    )    
]



async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Cyprus Weather sensors based on a config entry."""
    #conf_name = entry.data.get(CONF_NAME, hass.config.location_name)
    coordinator = hass.data[DOMAIN][entry.entry_id]
    city = entry.data.get(CONF_CITY)

    entities= []

    # Add all meter sensors described above.
    for weather_sensor in weather_sensors:
        entities.append(
            WeatherSensor(
                city=city,
                coordinator=coordinator,
                entry_id=entry.entry_id,
                description=weather_sensor,
            )
        )

    for air_quality_sensor in air_quality_sensors:
        entities.append(
            AirQualitySensor(
                city=city,
                coordinator=coordinator,
                entry_id=entry.entry_id,
                description=air_quality_sensor,
                definition='Malaka'
            )
        )

    async_add_entities(entities)



class WeatherSensor(CoordinatorEntity[CyprusWeatherUpdateCoordinator], SensorEntity):
    """Defines a WeatherSensor ."""

    _attr_has_entity_name = True

    def __init__(
        self,
        city: str,
        coordinator: CyprusWeatherUpdateCoordinator,
        entry_id: str,
        description: SensorEntityDescription,
    ) -> None:
        
        """Initialize Weather sensor."""
        super().__init__(coordinator=coordinator)

        self.entity_id = (
            f"{SENSOR_DOMAIN}.{city}_{description.name}".lower()
        )
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}-{DEFAULT_NAME} {city} {self.name}"
        #self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.get_weather_value(self.entity_description.key)



class AirQualitySensor(CoordinatorEntity[CyprusWeatherUpdateCoordinator], SensorEntity):
    """Defines a WeatherSensor ."""

    _attr_has_entity_name = True

    def __init__(
        self,
        city: str,
        coordinator: CyprusWeatherUpdateCoordinator,
        entry_id: str,
        description: SensorEntityDescription,
        definition: str,
    ) -> None:
        
        """Initialize Weather sensor."""
        super().__init__(coordinator=coordinator)

        self.entity_id = (
            f"{SENSOR_DOMAIN}.{city}_{description.name}".lower()
        )
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}-{DEFAULT_NAME} {city} {self.name}"
        #self._attr_device_info = coordinator.device_info

        self._attributes = {}
        self._attributes['definition'] = definition

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        d = self.coordinator.get_air_quality_value(self.entity_description.key)
        if 'value' in d:
            return d['value']
        return None
    
    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._attributes
