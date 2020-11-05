"""Platform for switch integration."""
import logging

import voluptuous

import homeassistant.helpers.config_validation
# Import the device class from the component that you want to support
from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .cvrky_controller_control import CvrkyControllerControl, CvrkyControllerControlItem

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    voluptuous.Required(CONF_HOST): homeassistant.helpers.config_validation.string,
})


# noinspection PyUnusedLocal
async def async_setup_entry(hass:HomeAssistant, config_entry:ConfigEntry, async_add_entities):
    ctl = CvrkyControllerControl(config_entry.data["host"])
    async_add_entities([CvrkyController(ctli) for ctli in await ctl.list()], True)
    return True


# noinspection PyAbstractClass
class CvrkyController(SwitchEntity):
    def __init__(self, ctli: CvrkyControllerControlItem):
        self._ctli = ctli
        self._name = "CvrkyController " + ctli.name.capitalize()
        self._id = str(self._name)
        self._status = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self) -> str:
        return self._id

    @property
    def device_info(self):
        return {
            'identifiers': {("cover", self._id)},
            'name': self._name,
            'manufacturer': 'Cvrky',
            'model': "Controller",
        }

    @property
    def is_on(self):
        return self.status

    async def async_turn_off(self, **kwargs):
        await self.async_toggle()

    async def async_turn_on(self, **kwargs):
        await self.async_toggle()

    async def async_toggle(self, **kwargs):
        await self._ctli.toggle()

    async def async_update(self):
        self.status = await self._ctli.is_on()
