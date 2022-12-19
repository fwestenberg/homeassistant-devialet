"""Constants for the Devialet integration."""
import logging
from typing import Final

DOMAIN: Final = "devialet"
DEFAULT_NAME: Final = "Devialet"
DEFAULT_SCAN_INTERVAL = 5
MANUFACTURER: Final = "Devialet"
LOGGER = logging.getLogger(__package__)

SOUND_MODES = {
    "Custom": "custom",
    "Flat": "flat",
    "Night mode": "night mode",
    "Voice": "voice",
}
