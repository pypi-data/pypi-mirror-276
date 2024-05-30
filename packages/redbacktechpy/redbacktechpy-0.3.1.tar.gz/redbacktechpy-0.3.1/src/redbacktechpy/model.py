""" Data classes for Redback Tech API """
from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Any, Optional


@dataclass
class Site:
    """Dataclass for Redback Sites."""

    id: str
    data: dict[str, Any]
    type: str
    
@dataclass
class Inverters:
    """Dataclass for Redback Inverters."""

    id: str
    device_serial_number: str
    data: dict[str, Any]
    type: str

@dataclass    
class Batterys:
    """Dataclass for RedBack Batteries."""

    id: str
    device_serial_number: str
    data: dict[str, Any]
    type: str

@dataclass
class DeviceInfo:
    """Dataclass for Device Info."""

    id: str
    device_serial_number: str
    data: dict[str, Any]
    type: str