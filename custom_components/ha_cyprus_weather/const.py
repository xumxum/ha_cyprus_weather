"""Constants."""
from datetime import timedelta

# API
# API_CONF_URL: Final = "https://weerlive.nl/api/toegang/account.php"
# API_ENDPOINT: Final = "https://weerlive.nl/api/json-data-10min.php?key={}&locatie={},{}"
# API_TIMEOUT: Final = 10
# API_TIMEZONE: Final = "Europe/Amsterdam"

# Base component constants.
NAME = "Cyprus Weather"
DOMAIN = "ha_cyprus_weather"
VERSION = "1.0.0"

CONF_CITY = "city"

# Defaults
DEFAULT_NAME = NAME
SCAN_INTERVAL: timedelta = timedelta(seconds=300)