"""Constants for the Devialet integration."""
from typing import Final

DOMAIN: Final = "devialet"
DEFAULT_SCAN_INTERVAL: Final = 5
MIN_SCAN_INTERVAL: Final = 1
MANUFACTURER: Final = "Devialet"

SOUND_MODES = {
    "Custom": "custom",
    "Flat": "flat",
    "Night mode": "night mode",
    "Voice": "voice",
}
