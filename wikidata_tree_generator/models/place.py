#!/usr/bin/env python3
from dataclasses import dataclass
from wikidata.entity import EntityId


@dataclass
class Place:
    id: EntityId
    name: str = None
    latitude: float = None
    longitude: float = None
