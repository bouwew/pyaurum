"""Support for the Aurum service."""
import logging

from homeassistant.helpers.entity import Entity

from .const import (
    ATTR_MANUFACTURER,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

SENSOR_MAP = {
    "powerBattery": ["Battery Power", "W", DEVICE_CLASS_POWER, "mdi:flash"],
    "counterOutBattery": ["Battery Counter out", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "counterInBattery": ["Battery Counter in", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "powerMCHP": ["MCHP Power", "W", DEVICE_CLASS_POWER, "mdi:flash"],
    "counterOutMCHP": ["MCHP Counter out", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "counterInMCHP": ["MCHP counter in", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "powerSolar": ["Solar Power", "W", DEVICE_CLASS_POWER, "mdi:flash"],
    "counterOutSolar": ["Solar Counter out", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "counterInSolar": ["Solar_Counter in", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "powerEV value": ["EV Power", "W", DEVICE_CLASS_POWER, "mdi:flash"],
    "counterOutEV": ["EV Counter out", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "counterInEV": ["EV Counter in", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "powerMain": ["Main Power", "W", DEVICE_CLASS_POWER, "mdi:flash"],
    "counterOutMain": ["Main Counter out", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "counterInMain value":["Main Counter in", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "smartMeterTimestamp": ["Dmartmeter timestamp", None, None, "mdi:av-timer"],
    "powerElectricity": ["Elec power", "W", DEVICE_CLASS_POWER, "mdi:flash"],
    "counterElectricityInLow": ["Elec Counter in low", "kWh", DEVICE_CLASS_POWER, "mdi:gauge"],
    "counterElectricityOutLow": ["Elec Cunter out low", "kWh",  DEVICE_CLASS_POWER, "mdi:gauge"],
    "counterElectricityInHigh":["Elec Counter in high", "kWh", DEVICE_CLASS_POWER, "mdi:gauge"],
    "counterElectricityOutHigh": ["Elec Counter out high", "kWh", DEVICE_CLASS_POWER, "mdi:gauge"],
    "rateGas": ["Gas consumption", "m3/h", DEVICE_CLASS_GAS, "mdi:fire"],
    "counterGas": ["Gas Counter", "m3", DEVICE_CLASS_GAS, "mdi:gauge"],
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add Aurum entities from a config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = []

    device_info = {
        "identifiers": {(DOMAIN, "00001")},
        "name": "Meetstekker",
        "manufacturer": ATTR_MANUFACTURER,
    }

    for sensor, sensor_type in SENSOR_MAP.items():
        _LOGGER.debug("data: %s", coordinator.data)
        if sensor in coordinator.data:
            sensors.append(AurumSensor(coordinator, sensor, device_info))
            _LOGGER.info("Added sensor.%s", "{}_{}".format("aurum", sensor))
    async_add_entities(sensors, False)


class AurumSensor(Entity):
    """Define an Brother Printer sensor."""

    def __init__(self, coordinator, kind, device_info):
        """Initialize."""
        self._name = f"{coordinator.data[ATTR_MODEL]} {SENSOR_TYPES[kind][ATTR_LABEL]}"
        self._unique_id = f"{coordinator.data[ATTR_SERIAL].lower()}"
        self._device_info = device_info
        self.coordinator = coordinator

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def icon(self):
        """Return the icon."""
        return SENSOR_MAP[ATTR_ICON]

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        return self._unique_id

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return SENSOR_MAP[ATTR_UNIT]

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def should_poll(self):
        """Return the polling requirement of the entity."""
        return False

#    @property
#    def device_info(self):
#        """Return the device info."""
#        return self._device_info

    @property
    def entity_registry_enabled_default(self):
        """Return if the entity should be enabled when first added to the entity registry."""
        return True

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Disconnect from update signal."""
        self.coordinator.async_remove_listener(self.async_write_ha_state)

    async def async_update(self):
        """Update Brother entity."""
        await self.coordinator.async_request_refresh()
