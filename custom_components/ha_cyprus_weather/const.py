"""Constants."""
from datetime import timedelta

# Base component constants.
NAME = "Cyprus Weather"
DOMAIN = "ha_cyprus_weather"

CONF_CITY = "city"

# Defaults
DEFAULT_NAME = NAME
SCAN_INTERVAL: timedelta = timedelta(seconds=60*30)