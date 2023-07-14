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


DESCRIPTIONS: list[SensorEntityDescription] = [
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
    for description in DESCRIPTIONS:
        entities.append(
            WeatherSensor(
                city=city,
                coordinator=coordinator,
                entry_id=entry.entry_id,
                description=description,
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
