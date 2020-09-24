#!/usr/bin/env python3
from dataclasses import dataclass

from .entity import Entity
from ..macros import PropertyTag


@dataclass
class CoordinateLocation:
    latitude: float = None
    longitude: float = None


class Place(Entity):
    PROPERTIES = [
        PropertyTag.COORDINATE_LOCATION
    ]
