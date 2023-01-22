"""Support for Devialet Phantom speakers."""
from __future__ import annotations
from datetime import timedelta

import datetime

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.config_entries import ConfigEntry

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    MANUFACTURER,
    SOUND_MODES,
    LOGGER,
)

from devialet.const import NORMAL_INPUTS
from devialet.devialet_api import DevialetApi

SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

SUPPORT_DEVIALET = (
    MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.SELECT_SOURCE
    | MediaPlayerEntityFeature.SELECT_SOUND_MODE
)

SUPPORT_MEDIA_MODES = (
    MediaPlayerEntityFeature.PAUSE
    | MediaPlayerEntityFeature.STOP
    | MediaPlayerEntityFeature.PREVIOUS_TRACK
    | MediaPlayerEntityFeature.NEXT_TRACK
    | MediaPlayerEntityFeature.PLAY
    | MediaPlayerEntityFeature.SEEK
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Devialet entry."""
    session = async_get_clientsession(hass)

    async_add_entities(
        [
            DevialetDevice(
                entry.data[CONF_HOST], entry.data[CONF_NAME], entry.unique_id, session
            )
        ],
        update_before_add=True,
    )


class DevialetDevice(MediaPlayerEntity):
    """Representation of a Devialet device."""

    def __init__(self, host, name, serial, session):
        """Initialize the Devialet device."""
        self._api = DevialetApi(host, session)
        self._name = name
        self._serial = serial
        self._muted = False

    async def async_update(self):
        """Get the latest details from the device."""
        await self._api.async_update()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._serial)},
            name=self._name,
            manufacturer=MANUFACTURER,
            model=self._api.model,
            sw_version=self._api.version,
        )

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of the device."""
        return self._serial

    @property
    def state(self) -> MediaPlayerState | None:
        """Return the state of the device."""
        if not self._api.is_available:
            return MediaPlayerState.OFF

        playing_state = self._api.playing_state

        if not playing_state:
            return MediaPlayerState.IDLE
        if playing_state == "playing":
            return MediaPlayerState.PLAYING
        if playing_state == "paused":
            return MediaPlayerState.PAUSED
        return MediaPlayerState.ON

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._api.volume_level

    @property
    def is_volume_muted(self):
        """Return boolean if volume is currently muted."""
        return self._api.is_volume_muted

    @property
    def source_list(self):
        """Return the list of available input sources."""
        return self._api.source_list

    @property
    def sound_mode_list(self):
        """Return the list of available sound modes."""
        return sorted(SOUND_MODES)

    @property
    def media_artist(self) -> str | None:
        """Artist of current playing media, music track only."""
        return self._api.media_artist

    @property
    def media_album_name(self) -> str | None:
        """Album name of current playing media, music track only."""
        return self._api.media_album_name

    @property
    def media_title(self):
        """Return the current media info."""
        if not self._api.media_title:
            return self.source

        return self._api.media_title

    @property
    def media_image_url(self) -> str | None:
        """Image url of current playing media."""
        return self._api.media_image_url

    @property
    def media_duration(self) -> int | None:
        """Duration of current playing media in seconds."""
        return self._api.media_duration

    @property
    def media_position(self) -> int | None:
        """Position of current playing media in seconds."""
        return self._api.current_position

    @property
    def media_position_updated_at(self) -> datetime.datetime | None:
        """When was the position of the current playing media valid."""
        return self._api.position_updated_at

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        """Flag media player features that are supported."""
        features = SUPPORT_DEVIALET

        if self._api.source_state is None:
            return features

        available_options = self._api.available_options
        if available_options is None:
            return features

        if "play" in available_options:
            features = features | MediaPlayerEntityFeature.PLAY
        if "pause" in available_options:
            features = (
                features
                | MediaPlayerEntityFeature.PAUSE
                | MediaPlayerEntityFeature.STOP
            )
        if "previous" in available_options:
            features = features | MediaPlayerEntityFeature.PREVIOUS_TRACK
        if "next" in available_options:
            features = features | MediaPlayerEntityFeature.NEXT_TRACK
        if "seek" in available_options:
            features = features | MediaPlayerEntityFeature.SEEK
        return features

    @property
    def source(self):
        """Return the current input source."""
        source = self._api.source

        for pretty_name, name in NORMAL_INPUTS.items():
            if source == name:
                return pretty_name

    @property
    def sound_mode(self):
        """Return the current sound mode."""
        if self._api.equalizer is not None:
            sound_mode = self._api.equalizer
        elif self._api.night_mode:
            sound_mode = "night mode"
        else:
            return None

        for pretty_name, mode in SOUND_MODES.items():
            if sound_mode == mode:
                return pretty_name

    async def async_volume_up(self) -> None:
        """Volume up media player."""
        await self._api.async_volume_up()

    async def async_volume_down(self) -> None:
        """Volume down media player."""
        await self._api.async_volume_down()

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        await self._api.async_set_volume_level(volume)

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute (true) or unmute (false) media player."""
        await self._api.async_mute_volume(mute)

    async def async_media_play(self) -> None:
        """Play media player."""
        await self._api.async_media_play()

    async def async_media_pause(self) -> None:
        """Pause media player."""
        await self._api.async_media_pause()

    async def async_media_stop(self) -> None:
        """Pause media player."""
        await self._api.async_media_stop()

    async def async_media_next_track(self) -> None:
        """Send the next track command."""
        await self._api.async_media_next_track()

    async def async_media_previous_track(self) -> None:
        """Send the previous track command."""
        await self._api.async_media_previous_track()

    async def async_media_seek(self, position: float) -> None:
        """Send seek command."""
        await self._api.async_media_seek(position)

    async def async_select_sound_mode(self, sound_mode: str) -> None:
        """Send sound mode command."""
        LOGGER.info(sound_mode)
        for pretty_name, mode in SOUND_MODES.items():
            if sound_mode == pretty_name:
                if mode == "night mode":
                    await self._api.async_set_night_mode(True)
                else:
                    await self._api.async_set_night_mode(False)
                    await self._api.async_set_equalizer(mode)

    async def async_turn_off(self) -> None:
        """Turn off media player."""
        await self._api.async_turn_off()

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        await self._api.async_select_source(source)
