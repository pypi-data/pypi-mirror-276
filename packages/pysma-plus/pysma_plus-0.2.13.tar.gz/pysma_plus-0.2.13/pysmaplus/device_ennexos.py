"""Interface for SMA ennoxOS based devices.

e.g. Tripower X and maybe EV Charger.
"""

import asyncio
import copy
import json
import logging
import re
from datetime import UTC, datetime
from typing import Any, Dict, Optional

from aiohttp import ClientSession, ClientTimeout, client_exceptions, hdrs

from .const import SMATagList
from .const_webconnect import DEFAULT_TIMEOUT
from .definitions_ennexos import ennexosSensorProfiles
from .device import Device, DiscoveryInformation
from .exceptions import (
    SmaAuthenticationException,
    SmaConnectionException,
    SmaReadException,
)
from .sensor import Sensor, Sensor_Range, Sensors

_LOGGER = logging.getLogger(__name__)


class SMAennexos(Device):
    """Class to connect to the ennexos based SMA inverters."""

    # pylint: disable=too-many-instance-attributes
    _aio_session: ClientSession
    _new_session_data: Optional[dict[str, Any]]
    _url: str
    _token: str
    _authorization_header: dict[str, str]
    _last_parameters: Any = {}
    _last_parameters_raw: Any = {}
    _last_measurements: Any = {}
    _last_measurements_raw: Any = {}
    _last_device: Any = {}
    _last_notfound: list = []
    _device_info: Dict[str, Any] | None = None
    _jsessionid: str | None = None
    _options: Dict[str, Any] = {}
    _readings: Dict[str, Dict[str, Any]] = {}

    def __init__(
        self,
        session: ClientSession,
        url: str,
        password: str | None,
        group: str | None,
    ):
        """Init SMA connection.

        Args:
            session (ClientSession): aiohttp client session
            url (str): Url or IP address of device
            password (str, optional): Password to use during login.
            group (str, optional): Username to use during login.

        """
        self._url = url.rstrip("/")
        if not url.startswith("http"):
            self._url = "https://" + self._url
        self._new_session_data = {"user": group, "pass": password}
        self._aio_session = session

    async def _jsonrequest(
        self, url: str, parameters: Dict[str, Any], method: str = hdrs.METH_POST
    ) -> Any:
        """Request json data for requests.

        Args:
            url (str): URL to do request to
            parameters (Dict[str, Any]): parameters
            method (str): Post or Get-Request

        Raises:
            SmaConnectionException: Connection to device failed
            SmaAuthenticationException: Authentication failed

        Returns:
            dict: json returned by device
        """
        try:
            async with self._aio_session.request(
                method, url, timeout=ClientTimeout(total=DEFAULT_TIMEOUT), **parameters
            ) as res:
                if res.status == 401:
                    raise SmaAuthenticationException("Token failed!")
                res = await res.json()
                # _LOGGER.debug("Received reply %s", res)
                return res
        except SmaAuthenticationException as e:
            raise e
        except (client_exceptions.ContentTypeError, json.decoder.JSONDecodeError):
            _LOGGER.warning("Request to %s did not return a valid json.", url)
        except client_exceptions.ServerDisconnectedError as exc:
            raise SmaConnectionException(
                f"Server at {self._url} disconnected."
            ) from exc
        except (
            client_exceptions.ClientError,
            asyncio.exceptions.TimeoutError,
        ) as exc:
            raise SmaConnectionException(
                f"Could not connect to SMA at {self._url}: {exc}"
            ) from exc
        return {}

    async def new_session(self) -> bool:
        """Establish a new session.

        Returns:
            bool: authentication successful
        """
        if self._new_session_data is None:
            _LOGGER.error("User & Pwd not set!")
            return False
        loginurl = self._url + "/api/v1/token"
        postdata = {
            "data": {
                "grant_type": "password",
                "username": self._new_session_data["user"],
                "password": self._new_session_data["pass"],
            }
        }
        ret = await self._jsonrequest(loginurl, postdata)
        if "access_token" not in ret:
            raise SmaAuthenticationException("Login failed!")
        self._token = ret["access_token"]
        #        self._refreshtoken = ret["refresh_token"]
        self._authorization_header = {
            "Authorization": "Bearer " + self._token,
            "Content-Type": "application/json",
        }
        _LOGGER.debug("Login successful")
        return True

    async def _get_parameter(self) -> Dict[str, Dict[str, Any]]:
        """Get all parameters from the device.

        Returns:
            Dict: Return a dict with all parameters

        """
        url = self._url + "/api/v1/parameters/search"
        postdata = {
            "data": '{"queryItems":[{"componentId":"IGULD:SELF"}]}',
            "headers": self._authorization_header,
        }
        ret = await self._jsonrequest(url, postdata)
        self._last_parameters_raw = ret
        data = {}
        if len(ret) != 1:
            _LOGGER.warning(
                "Uncommon length of array in parameters request: %d", len(ret)
            )

        for d in ret[0]["values"]:
            dname = d["channelId"].replace("Parameter.", "").replace("[]", "")
            if "value" in d:
                v = d["value"]
                sensor_range = Sensor_Range("", [], d["editable"])
                if "min" in d and "max" in d:
                    sensor_range = Sensor_Range(
                        "min/max", [d["min"], d["max"]], d["editable"]
                    )
                if "possibleValues" in d:
                    sensor_range = Sensor_Range(
                        "selection", d["possibleValues"], d["editable"]
                    )

                data[dname] = {
                    "name": dname,
                    "value": v,
                    "origname": d["channelId"],
                    "range": sensor_range,
                }

            elif "values" in d:
                # Split Value-Arrays
                for idx in range(0, len(d["values"])):
                    v = d["values"][idx]
                    idxname = dname + "." + str(idx + 1)
                    data[idxname] = {
                        "name": idxname,
                        "value": v,
                        "origname": d["channelId"],
                    }
            else:
                # Value current not available // night?
                pass
        return data

    async def _get_all_readings(self) -> Dict[str, Dict[str, Any]]:
        self._readings = await self._get_livedata()
        self._readings.update(await self._get_parameter())
        return self._readings

    async def _get_livedata(self) -> Dict[str, Dict[str, Any]]:
        """Get the sensors reading from the device.

        Returns:
            Dict: Return a dict with all measurements

        """
        liveurl = self._url + "/api/v1/measurements/live"
        postdata = {
            "data": '[{"componentId":"IGULD:SELF"}]',
            "headers": self._authorization_header,
        }
        ret = await self._jsonrequest(liveurl, postdata)
        self._last_measurements_raw = ret
        return await self._prepare_livedata(ret)

    async def _prepare_livedata(self, ret: Any) -> Dict[str, Dict[str, Any]]:
        """Convert the raw data from the inverter to a dict"""
        self._last_measurements = ret
        data: Dict[str, Any] = {}
        for d in ret:
            dname = d["channelId"].replace("Measurement.", "").replace("[]", "")
            if "value" in d["values"][0]:
                v = d["values"][0]["value"]
                if self._isfloat(v):
                    v = round(v, 2)
                data[dname] = {"name": dname, "value": v, "origname": d["channelId"]}
            elif "values" in d["values"][0]:
                # Split Value-Arrays
                for idx in range(0, len(d["values"][0]["values"])):
                    v = d["values"][0]["values"][idx]
                    if self._isfloat(v):
                        v = round(v, 2)
                    idxname = dname + "." + str(idx + 1)
                    data[idxname] = {
                        "name": idxname,
                        "value": v,
                        "origname": d["channelId"],
                    }
            else:
                # Value current not available // night?
                pass
        return data

    async def get_sensors(self) -> Sensors:
        """Get the sensors that are present on the device.

        Returns:
            Sensors: Sensors object containing Sensor objects
        """
        if not self._device_info:
            raise SmaReadException("device_info() not called!")

        ret = await self._get_all_readings()
        _LOGGER.debug("Found Sensors: %s", ret)
        profile = await self._get_sensor_profile()
        return profile

    async def _get_sensor_profile(self) -> Sensors:
        device_sensors = Sensors()
        expected_sensors = []

        # Search for matiching profile
        if self._device_info:
            if "name" in self._device_info:
                for profil in ennexosSensorProfiles.items():
                    if re.search(profil[0], self._device_info["name"]):
                        expected_sensors = profil[1]
            if len(expected_sensors) == 0:
                _LOGGER.warning(
                    f'Unknown Device: {self._device_info["name"]} {self._device_info["type"]}'
                )

        # Add Sensors from profile
        for s in expected_sensors:
            if s.name:
                device_sensors.add(copy.copy(s))
        return device_sensors

    async def close_session(self) -> None:
        """Closes the session."""

    def _isfloat(self, num: Any) -> bool:
        """Test if num is a float.

            Tests for type float or a string with a dot is is float

        Args:
            num: number to check

        Returns:
            bool: true, if num is from type float or a string with a dot
        """
        if isinstance(num, float):
            return True
        if isinstance(num, int):
            return False
        if not isinstance(num, str):
            raise TypeError("Value is not a string, float or int!")
        if "." not in num:
            return False
        try:
            float(num)
            return True
        except ValueError:
            return False

    async def read(self, sensors: Sensors) -> bool:
        """Read a set of keys.

        Args:
            sensors (Sensors): Sensors object containing Sensor objects to read

        Returns:
            bool: reading was successful
        """
        notfound = []
        data = None
        try:
            data = await self._get_all_readings()
        except SmaAuthenticationException:
            # Relogin
            _LOGGER.debug("Re-login .. Starting new Session")
            await self.new_session()
            data = await self._get_all_readings()
        for sen in sensors:
            if sen.enabled:
                if sen.key in data:
                    value = data[sen.key]["value"]
                    if sen.mapper:
                        sen.mapped_value = sen.mapper.get(value, str(value))
                    if sen.factor and sen.factor != 1:
                        value = round(value / sen.factor, 4)
                    sen.value = value
                    if "range" in data[sen.key]:
                        sen.range = data[sen.key]["range"]
                    continue
                notfound.append(f"{sen.name} [{sen.key}]")

        self._last_notfound = notfound
        if notfound:
            _LOGGER.info(
                "No values for sensors: %s",
                ",".join(notfound),
            )

        return True

    async def device_info(self) -> dict:
        """Read device info and return the results.

        Returns:
            dict: dict containing serial, name, type, manufacturer and sw_version
        """
        url = self._url + "/api/v1/plants/Plant:1/devices/IGULD:SELF"
        requestdata = {"headers": self._authorization_header}
        dev = await self._jsonrequest(url, requestdata, hdrs.METH_GET)
        self._last_device = dev
        self._last_parameters = await self._get_parameter()
        _LOGGER.debug("Found Device: %s", dev)
        self._device_info = {
            "serial": dev["serial"],
            "name": dev["product"],
            "type": dev["name"],
            "manufacturer": dev["vendor"],
            "sw_version": dev["firmwareVersion"],
        }
        return self._device_info

    async def get_debug(self) -> Dict:
        """Returns all Debug Information."""
        return {
            "device": self._last_device,
            "measurements": self._last_measurements,
            "parameters": self._last_parameters,
            "measurements_raw": self._last_measurements_raw,
            "parameters_raw": self._last_parameters_raw,
            "device_info": self._device_info,
            "notfound": self._last_notfound,
        }

    async def detect(self, ip: str) -> list[DiscoveryInformation]:
        """Tries to detect a ennexos-based Device on this ip-address."""
        rets = []
        for prefix in ["https", "http"]:
            di = DiscoveryInformation()
            rets.append(di)
            url = f"{prefix}://{ip}/api/v1/system/info"
            di.tested_endpoints = url
            di.remark = prefix
            try:
                dev = await self._jsonrequest(url, {}, hdrs.METH_GET)
                if "productFriendlyNameTagId" in dev:
                    fallback = "Unknown: " + str(dev["productFriendlyNameTagId"])
                    di.device = SMATagList.get(
                        dev["productFriendlyNameTagId"], fallback
                    )
                    di.status = "found"
                    break
                di.status = "failed"
                di.exception = None
            except Exception as e:  # pylint: disable=broad-exception-caught
                di.status = "failed"
                di.exception = e
        return rets

    def set_options(self, options: Dict[str, Any]) -> None:
        """Set low-level options."""
        self._options = options

    async def _get_timestamp(self) -> str:
        """Returns the time in a format as required by the put instruction."""
        return (
            f"{datetime.now(tz=UTC).isoformat(timespec='milliseconds').split('+')[0]}Z"
        )

    async def set_parameter(self, sensor: Sensor, value: int) -> None:
        """SetParameters."""
        timestamp = await self._get_timestamp()
        channelName = self._readings[sensor.key]["origname"]
        requestData = f'{{"values":[{{"channelId":"{channelName}","timestamp":"{timestamp}","value":"{value}"}}]}}'
        putdata = {
            "data": requestData,
            "headers": self._authorization_header,
        }
        url = self._url + "/api/v1/parameters/IGULD:SELF"
        dev = await self._jsonrequest(url, putdata, hdrs.METH_PUT)
        print(dev)
