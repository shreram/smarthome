from datetime import timedelta
import logging
import subprocess

import voluptuous as vol


from homeassistant.helpers import template
from homeassistant.exceptions import TemplateError
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, CONF_VALUE_TEMPLATE, CONF_UNIT_OF_MEASUREMENT, 
    STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Life360 Sensor'

SCAN_INTERVAL = timedelta(seconds=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required("username"): cv.string,
    vol.Required("password"): cv.string,
    vol.Required("command1"): cv.string,
    vol.Required("command2"): cv.string,
    vol.Required("command3"): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
})


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Life360 Sensor."""
    name = config.get(CONF_NAME)
    username = config.get("username")
    password = config.get("password")
    command1 = config.get("command1")
    command2 = config.get("command2")
    command3 = config.get("command3")
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)
    value_template = config.get(CONF_VALUE_TEMPLATE)
    if value_template is not None:
        value_template.hass = hass

    data = Life360SensorData(username, password, command1, command2, command3, hass)

    add_devices([Life360Sensor(hass, data, name, unit, value_template)])


class Life360Sensor(Entity):
    """Representation of a sensor."""

    def __init__(self, hass, data, name, unit_of_measurement, value_template):
        """Initialize the sensor."""
        self._hass = hass
        self.data = data
        self._name = name
        self._state = STATE_UNKNOWN
        self._unit_of_measurement = unit_of_measurement
        self._value_template = value_template
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def update(self):
        """Get the latest data and updates the state."""
        self.data.update()
        value = self.data.value

        if value is None:
            value = STATE_UNKNOWN
        elif self._value_template is not None:
            self._state = self._value_template.render_with_possible_json_value(
                value, STATE_UNKNOWN)
        else:
            self._state = value


class Life360SensorData(object):
    """The class for handling the data retrieval."""

    def __init__(self, username, password, command1, command2, command3, hass):
        """Initialize the data object."""
        self.username = username
        self.password = password
        self.command1 = command1
        self.command2 = command2
        self.command3 = command3
        self.hass = hass
        self.value = None

    def update(self):

        self.command1 = self.command1.replace("USERNAME360", self.username)
        self.command1 = self.command1.replace("PASSWORD360", self.password)

        try:
            """Get the latest data with a shell command."""
            _LOGGER.info("Running command 1: %s", self.command1)

            return_value = subprocess.check_output(
                self.command1, shell=True, timeout=15)
            access_token = return_value.strip().decode('utf-8')

            self.command2 = self.command2.replace("ACCESS_TOKEN", access_token)
            _LOGGER.info("Running command 2: %s", self.command2)

            return_value = subprocess.check_output(
                self.command2, shell=True, timeout=15)
            id = return_value.strip().decode('utf-8')

            self.command3 = self.command3.replace("ACCESS_TOKEN", access_token)
            self.command3 = self.command3.replace("ID", id)

            _LOGGER.info("Running command 3: %s", self.command3)
            return_value = subprocess.check_output(
                self.command3, shell=True, timeout=15)
            self.value = return_value.strip().decode('utf-8')

        except subprocess.CalledProcessError:
            _LOGGER.error("Command failed: %s", self.command1)
        except subprocess.TimeoutExpired:
            _LOGGER.error("Timeout for command: %s", self.command1)
