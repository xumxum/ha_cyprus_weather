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

from homeassistant.const import CONF_NAME, PERCENTAGE
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant


from homeassistant.util.enum import try_parse_enum

from .const import DEFAULT_NAME, DOMAIN, CONF_CITY
from .coordinator import CyprusWeatherUpdateCoordinator
from .air_quality import get_air_quality_parameters

_LOGGER = logging.getLogger(__name__)


weather_sensors: list[SensorEntityDescription] = [
    SensorEntityDescription(
        key="Current.Temperature",
        name="Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Current.Humidity",
        name="Humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY, 
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Current.Pressure",
        name="Pressure",
        native_unit_of_measurement='hPa',
        device_class=SensorDeviceClass.PRESSURE, 
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Current.Wind",
        name="Wind Speed",
        native_unit_of_measurement='km/h',
        device_class=SensorDeviceClass.WIND_SPEED, #?
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="Current.FeelsLike",
        name="Feels Like",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    )
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Cyprus Weather sensors based on a config entry."""
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

    # Add the Air Quality sensors from the file 
    air_quality_sensors = get_air_quality_parameters()

    for air_quality_sensor in air_quality_sensors:
            entities.append(
                AirQualitySensor(
                    city=city,
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    name = air_quality_sensor,
                    description=air_quality_sensors[air_quality_sensor],
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

        _LOGGER.debug(f"Setting up WeatherSensor: name: {description.name} key: {description.key} device_class: {self.entity_description.device_class}")      

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.get_weather_value(self.entity_description.key)



class AirQualitySensor(CoordinatorEntity[CyprusWeatherUpdateCoordinator], SensorEntity):
    """Defines a AirQualitySensor ."""

    #_attr_has_entity_name = True

    def __init__(
        self,
        city: str,
        coordinator: CyprusWeatherUpdateCoordinator,
        entry_id: str,
        name: str,
        description: dict
    ) -> None:
        
        """Initialize AirQualitySensor."""
        super().__init__(coordinator=coordinator)

        self._name = name

        self.entity_id = (
            f"{SENSOR_DOMAIN}.{city}_{name}".lower()
        )

        self.description = description

        self.entity_description = SensorEntityDescription(
            key = self._name,
            name=self._name,
            native_unit_of_measurement = self.description['unit_of_measurement'],
            device_class = try_parse_enum(SensorDeviceClass, description['device_class']),
            state_class=SensorStateClass.MEASUREMENT,
        )  
        self._attr_unique_id = f"{entry_id}-{DEFAULT_NAME} {city} {self._name}"
        
        self._attributes = {}
        self._attributes['description'] = description['description']

        _LOGGER.debug(f"Setting up AirQualitySensor: name: {self._name} key: {self.entity_description.key} device_class: {self.entity_description.device_class}")

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        d = self.coordinator.get_air_quality_value(self.entity_description.key)
        if d and 'value' in d:
            return d['value']
        return None

        
    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        d = self.coordinator.get_air_quality_value(self.entity_description.key)
        if d and 'polution_level' in d:
            self._attributes['polution_level'] = d['polution_level']
        return self._attributes
