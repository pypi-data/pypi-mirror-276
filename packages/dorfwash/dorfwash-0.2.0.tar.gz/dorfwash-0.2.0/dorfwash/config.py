from typing import List
from pydantic import BaseModel
from washpy.authenticate import DeviceUrl


class Device(BaseModel):
    """
    holds the config values for one machine
    """

    name: str
    """some name for the machine"""

    url: DeviceUrl
    """
    the URL of the machine,
    e.g. `'https://192.168.1.251/Devices/000116343328'`
    """

    username: str
    """
    login user name for the machine
    """

    password: str
    """
    login password
    """

    verify_https: bool | str = False
    """
    should dorfwash verify the SSL certificates of the machine
    """


class DorfwashConfig(BaseModel):
    """
    holds the configuration for the dorfwash application
    """

    https_timeout: float = 3.05
    """
    timeout for HTTPS connections, in seconds.
    """

    devices: List[Device]
    """
    list of all device configs
    """
