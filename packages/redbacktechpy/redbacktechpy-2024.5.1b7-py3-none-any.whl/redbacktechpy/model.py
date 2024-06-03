""" Data classes for Redback Tech API """
from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Any, Optional


@dataclass
class RedbackTechData:
    """Dataclass for all RedbackTech Data."""

    user_id: str
    inverters: Optional[dict[int, Any]] = None
    batterys: Optional[dict[int, Any]] = None
    entities: Optional[dict[int, Any]] = None
    devices: Optional[dict[int, Any]] = None

@dataclass
class Site:
    """Dataclass for Redback Sites."""

    id: str
    data: dict[str, Any]
    type: str

@dataclass
class RedbackEntitys:
    entity_id: str
    device_id: str
    data: dict[str, Any]
    type: Optional[str] = None
    device_data: Optional[dict[str, Any]] = None
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

    identifiers: str
    name: str
    model: str
    sw_version: str
    hw_version: str
    serial_number: str
