"""Adds config flow for knmi."""
import logging

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.helpers.selector import selector

# from .api import (
#     KnmiApiClient,
#     KnmiApiClientApiKeyError,
#     KnmiApiClientCommunicationError,
#     KnmiApiRateLimitError,
# )
from .const import DOMAIN, CONF_CITY

_LOGGER: logging.Logger = logging.getLogger(__package__)


class KnmiFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for knmi."""

    VERSION = 1

    async def async_step_user( self, user_input: dict | None = None ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        if user_input is not None:
            return self.async_create_entry( title=user_input[CONF_CITY], data=user_input )

        # data_schema={
        #                 vol.Required(
        #                     CONF_NAME, default="weather.limassol"
        #                 ): str
        # 
        #             }
        data_schema = {}
                    
        data_schema[CONF_CITY] = selector({
                        "select": {
                            "options": ["Limassol", "Nicosia", "Larnaca"],
                        }
                    })

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema),
            errors=_errors,
        )
    

    async def _validate_user_input(self, api_key: str, latitude: str, longitude: str):
        """Validate user input."""
        # session = async_create_clientsession(self.hass)
        # client = KnmiApiClient(api_key, latitude, longitude, session)
        # await client.async_get_data()
        return True