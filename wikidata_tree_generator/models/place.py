#!/usr/bin/env python3
from dataclasses import dataclass

from .entity import Entity, Properties


@dataclass
class CoordinateLocation:
    latitude: float = None
    longitude: float = None


class Place(Entity):
    PROPERTIES = [
        Properties.COORDINATE_LOCATION
    ]
